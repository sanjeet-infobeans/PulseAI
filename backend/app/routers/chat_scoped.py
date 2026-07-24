"""Unified 'Ask PulseAI' scope entry point — auto-detects role:
- super_admin: picks any combination of industry / customer / project. Fields
  narrow each other (industry + customer together = that customer's projects
  in that industry); picking a project wins outright (most specific).
- customer: always forced to their own customer_id, never industry-wide.
  Picks either "all my projects" (customer_id only) or one specific project.

Kept as a separate router/path from routers/chat.py (not an optional param on
the existing nested route) because that route's 404/403 checks are keyed on a
project_id path param that doesn't exist for these broader-scope sessions.
The existing per-project chat flow in chat.py is completely untouched — this
is purely additive, and project-scoped sessions created here are the exact
same ChatSession rows/shape chat.py already produces.
"""
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
from app.models.customer import Customer
from app.models.llm_call_log import LLMFeature
from app.models.user import User, UserRole
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services import chat_service
from app.services.retrieval import build_context_multi, resolve_project_ids

router = APIRouter(tags=["chat-scoped"])


class SessionOut(BaseModel):
    id: str
    title: str
    project_id: str | None
    customer_id: str | None
    industry: str | None
    created_at: str

    @classmethod
    def of(cls, s: ChatSession) -> "SessionOut":
        return cls(
            id=str(s.id), title=s.title,
            project_id=str(s.project_id) if s.project_id else None,
            customer_id=str(s.customer_id) if s.customer_id else None,
            industry=s.industry, created_at=s.created_at.isoformat(),
        )


class MessageOut(BaseModel):
    id: str
    role: str
    content: str
    citations: list
    created_at: str


class NewScopedSessionBody(BaseModel):
    project_id: uuid.UUID | None = None
    customer_id: uuid.UUID | None = None
    industry: str | None = None
    title: str = "New chat"


class AskBody(BaseModel):
    question: str


async def _resolve_session_scope(
    db: AsyncSession, session: ChatSession, user: User
) -> tuple[list[uuid.UUID], bool]:
    if session.project_id:
        await _load_project(db, session.project_id, user)  # enforces customer-role ownership
        return [session.project_id], False
    if user.role == UserRole.customer and session.customer_id != user.customer_id:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    project_ids, total_matched = await resolve_project_ids(
        db, customer_id=session.customer_id, industry=session.industry,
    )
    return project_ids, len(project_ids) < total_matched


async def _load_scoped_session(db: AsyncSession, sid: uuid.UUID, user: User) -> ChatSession:
    session = await db.get(ChatSession, sid)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    await _resolve_session_scope(db, session, user)  # raises 403 if out of scope
    return session


@router.post("/chat/sessions", response_model=SessionOut, status_code=201)
async def create_scoped_session(
    body: NewScopedSessionBody, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> SessionOut:
    if body.project_id:
        await _load_project(db, body.project_id, user)
        session = await chat_service.create_session(db, body.project_id, user.id, body.title)
        return SessionOut.of(session)

    if user.role == UserRole.customer:
        if body.industry:
            raise HTTPException(status_code=403, detail="Customers cannot use industry-wide chat")
        if body.customer_id and body.customer_id != user.customer_id:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        customer_id = user.customer_id
        industry = None
    else:
        customer_id = body.customer_id
        industry = body.industry

    if not customer_id and not industry:
        raise HTTPException(status_code=422, detail="Select at least one of industry, customer, or project")
    if customer_id and not await db.get(Customer, customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")

    session = await chat_service.create_scoped_session(
        db, customer_id=customer_id, industry=industry, user_id=user.id, title=body.title,
    )
    return SessionOut.of(session)


@router.get("/chat/sessions", response_model=list[SessionOut])
async def list_scoped_sessions(
    user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)],
    customer_id: uuid.UUID | None = None,
    industry: str | None = None,
) -> list[SessionOut]:
    if user.role == UserRole.customer:
        if industry:
            raise HTTPException(status_code=403, detail="Customers cannot use industry-wide chat")
        customer_id = user.customer_id  # always forced to own

    stmt = select(ChatSession).where(ChatSession.project_id.is_(None))
    if customer_id:
        stmt = stmt.where(ChatSession.customer_id == customer_id)
    if industry:
        stmt = stmt.where(ChatSession.industry == industry)
    stmt = stmt.order_by(ChatSession.created_at.desc())
    rows = (await db.execute(stmt)).scalars().all()
    return [SessionOut.of(s) for s in rows]


@router.get("/chat/sessions/{sid}/messages", response_model=list[MessageOut])
async def list_scoped_messages(
    sid: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)],
) -> list[MessageOut]:
    await _load_scoped_session(db, sid, user)
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


@router.post("/chat/sessions/{sid}/messages")
async def ask_scoped(
    sid: uuid.UUID, body: AskBody, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)],
) -> StreamingResponse:
    session = await _load_scoped_session(db, sid, user)
    project_ids, scope_truncated = await _resolve_session_scope(db, session, user)
    context = await build_context_multi(db, project_ids, scope_truncated=scope_truncated)
    history = await chat_service.load_history(db, session.id)
    await chat_service.add_message(db, session.id, ChatRole.user, body.question)
    messages = prompts.chat_messages(context, history, body.question)

    async def event_stream():
        parts: list[str] = []
        try:
            async for event in client.stream(
                feature=LLMFeature.chat, messages=messages,
                model=settings.llm_model_chat, project_id=project_ids[0] if len(project_ids) == 1 else None,
            ):
                if event["type"] == "delta":
                    parts.append(event["text"])
                    yield f"data: {json.dumps({'type': 'token', 'value': event['text']})}\n\n"
                elif event["type"] == "retry":
                    # A key/provider failed mid-response — the next attempt
                    # regenerates the full answer from scratch, so discard
                    # whatever partial text this attempt had produced.
                    parts = []
                    yield f"data: {json.dumps({'type': 'retry'})}\n\n"
        except Exception as exc:  # noqa: BLE001
            yield f"data: {json.dumps({'type': 'error', 'value': str(exc)})}\n\n"

        full = "".join(parts)
        citations = await chat_service.extract_citations_multi(db, project_ids, full)
        await chat_service.add_message(
            db, session.id, ChatRole.assistant, full, citations=citations,
            model=settings.llm_model_chat,
        )
        if citations:
            yield f"data: {json.dumps({'type': 'citations', 'value': citations})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
