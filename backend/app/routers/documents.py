import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import get_db
from app.models.document import Document, DocStatus, DocType
from app.routers.auth import CurrentUser
from app.routers.projects import _load_project
from app.services.document_service import detect_doc_type, process_document
from app.services.requirement_service import get_requirement_drift
from app.storage import supabase_storage

router = APIRouter(tags=["documents"])


class DocumentOut(BaseModel):
    id: str
    filename: str
    doc_type: str
    status: str
    error: str | None
    extraction: dict | None
    summary: str | None
    created_at: str

    @classmethod
    def of(cls, d: Document, extraction=None) -> "DocumentOut":
        return cls(
            id=str(d.id), filename=d.filename, doc_type=d.doc_type.value,
            status=d.status.value, error=d.error,
            extraction=extraction.extraction if extraction else None,
            summary=extraction.summary if extraction else None,
            created_at=d.created_at.isoformat(),
        )


@router.get("/projects/{project_id}/documents", response_model=list[DocumentOut])
async def list_documents(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> list[DocumentOut]:
    await _load_project(db, project_id, user)
    rows = (
        await db.execute(
            select(Document).where(Document.project_id == project_id)
            .options(selectinload(Document.extraction))
            .order_by(Document.created_at.desc())
        )
    ).scalars().all()
    return [DocumentOut.of(d, d.extraction) for d in rows]


@router.get("/documents/{document_id}", response_model=DocumentOut)
async def get_document(
    document_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> DocumentOut:
    doc = (
        await db.execute(
            select(Document).where(Document.id == document_id)
            .options(selectinload(Document.extraction))
        )
    ).scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await _load_project(db, doc.project_id, user)
    return DocumentOut.of(doc, doc.extraction)


@router.post("/projects/{project_id}/documents", response_model=DocumentOut, status_code=201)
async def upload_document(
    project_id: uuid.UUID,
    background: BackgroundTasks,
    user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...),
    doc_type: Annotated[DocType | None, Form()] = None,
) -> DocumentOut:
    await _load_project(db, project_id, user)
    content = await file.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File exceeds {settings.max_upload_mb} MB")

    # Uploader-selected category wins; fall back to filename detection.
    doc_type = doc_type or detect_doc_type(file.filename or "document")
    doc = Document(
        project_id=project_id,
        filename=file.filename or "document",
        doc_type=doc_type,
        mime_type=file.content_type,
        size_bytes=len(content),
        status=DocStatus.uploaded,
        uploaded_by=user.id,
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    doc.storage_path = supabase_storage.upload(
        f"{project_id}/{doc.id}/{doc.filename}", content, file.content_type
    )
    await db.commit()

    background.add_task(process_document, doc.id, content, file.content_type, doc.filename)
    return DocumentOut.of(doc)


@router.get("/projects/{project_id}/requirements/drift")
async def requirement_drift(
    project_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> list[dict]:
    await _load_project(db, project_id, user)
    return await get_requirement_drift(db, project_id)


@router.delete("/documents/{document_id}", status_code=204)
async def delete_document(
    document_id: uuid.UUID, user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    doc = await db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await _load_project(db, doc.project_id, user)
    # Best-effort remove from storage, then delete the row (extraction cascades).
    if doc.storage_path:
        supabase_storage.remove(doc.storage_path)
    await db.delete(doc)
    await db.commit()
