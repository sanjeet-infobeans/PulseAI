import re
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import ChatMessage, ChatRole, ChatSession
from app.models.story import Story

_MAX_HISTORY = 10


async def load_history(db: AsyncSession, session_id: uuid.UUID) -> list[dict]:
    rows = (
        await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(_MAX_HISTORY)
        )
    ).scalars().all()
    rows = list(reversed(rows))
    return [{"role": m.role.value, "content": m.content} for m in rows if m.role != ChatRole.system]


async def add_message(
    db: AsyncSession, session_id: uuid.UUID, role: ChatRole, content: str,
    citations: list | None = None, model: str | None = None,
) -> ChatMessage:
    msg = ChatMessage(
        session_id=session_id, role=role, content=content,
        citations=citations or [], model=model,
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


async def extract_citations(db: AsyncSession, project_id: uuid.UUID, text: str) -> list[dict]:
    """Find story keys the answer references (e.g. ATLAS-123) that exist in this project."""
    candidates = set(re.findall(r"\b[A-Z][A-Z0-9]+-\d+\b", text))
    if not candidates:
        return []
    rows = (
        await db.execute(
            select(Story.external_id, Story.title)
            .where(Story.project_id == project_id, Story.external_id.in_(candidates))
        )
    ).all()
    return [{"type": "jira", "ref": ext, "label": title} for ext, title in rows]


async def create_session(db: AsyncSession, project_id: uuid.UUID, user_id: uuid.UUID, title: str) -> ChatSession:
    session = ChatSession(project_id=project_id, user_id=user_id, title=title[:120] or "New chat")
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session
