import json
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.llm import client, prompts
from app.models.chat import ChatMessage, ChatRole, ChatSession
from app.models.llm_call_log import LLMFeature
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services import chat_service
from app.services.retrieval import build_context

router = APIRouter(tags=["chat"])


class SessionOut(BaseModel):
    id: str
    title: str
    created_at: str


class MessageOut(BaseModel):
    id: str
    role: str
    content: str
    citations: list
    created_at: str


class NewSessionBody(BaseModel):
    title: str = "New chat"


class AskBody(BaseModel):
    question: str


async def _load_session(db: AsyncSession, project_id: uuid.UUID, sid: uuid.UUID, user) -> ChatSession:
    await _load_project(db, project_id, user)
    session = await db.get(ChatSession, sid)
    if not session or session.project_id != project_id:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session


@router.get("/projects/{project_id}/chat/sessions", response_model=list[SessionOut])
async def list_sessions(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> list[SessionOut]:
    await _load_project(db, project_id, user)
    rows = (
        await db.execute(
            select(ChatSession).where(ChatSession.project_id == project_id)
            .order_by(ChatSession.created_at.desc())
        )
    ).scalars().all()
    return [SessionOut(id=str(s.id), title=s.title, created_at=s.created_at.isoformat()) for s in rows]


@router.post("/projects/{project_id}/chat/sessions", response_model=SessionOut, status_code=201)
async def create_session(
    project_id: uuid.UUID, body: NewSessionBody, user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SessionOut:
    await _load_project(db, project_id, user)
    s = await chat_service.create_session(db, project_id, user.id, body.title)
    return SessionOut(id=str(s.id), title=s.title, created_at=s.created_at.isoformat())


@router.get("/projects/{project_id}/chat/sessions/{sid}/messages", response_model=list[MessageOut])
async def list_messages(
    project_id: uuid.UUID, sid: uuid.UUID, user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[MessageOut]:
    await _load_session(db, project_id, sid, user)
    rows = (
        await db.execute(
            select(ChatMessage).where(ChatMessage.session_id == sid).order_by(ChatMessage.created_at)
        )
    ).scalars().all()
    return [
        MessageOut(id=str(m.id), role=m.role.value, content=m.content,
                   citations=m.citations or [], created_at=m.created_at.isoformat())
        for m in rows
    ]


@router.post("/projects/{project_id}/chat/sessions/{sid}/messages")
async def ask(
    project_id: uuid.UUID, sid: uuid.UUID, body: AskBody, user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> StreamingResponse:
    session = await _load_session(db, project_id, sid, user)
    context = await build_context(db, project_id)
    history = await chat_service.load_history(db, session.id)
    await chat_service.add_message(db, session.id, ChatRole.user, body.question)
    messages = prompts.chat_messages(context, history, body.question)

    async def event_stream():
        parts: list[str] = []
        try:
            async for delta in client.stream(
                feature=LLMFeature.chat, messages=messages,
                model=settings.llm_model_chat, project_id=project_id,
            ):
                parts.append(delta)
                yield f"data: {json.dumps({'type': 'token', 'value': delta})}\n\n"
        except Exception as exc:  # noqa: BLE001
            yield f"data: {json.dumps({'type': 'error', 'value': str(exc)})}\n\n"

        full = "".join(parts)
        # Persist in a fresh session (the request session is fine here since we awaited the stream)
        citations = await chat_service.extract_citations(db, project_id, full)
        await chat_service.add_message(
            db, session.id, ChatRole.assistant, full, citations=citations,
            model=settings.llm_model_chat,
        )
        if citations:
            yield f"data: {json.dumps({'type': 'citations', 'value': citations})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
