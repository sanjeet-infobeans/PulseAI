import io
import json
import logging
import uuid

from fastapi import HTTPException

from app.config import settings
from app.database import AsyncSessionLocal
from app.llm import client, prompts
from app.models.document import DocStatus, DocType, Document, DocumentExtraction
from app.models.llm_call_log import LLMFeature

logger = logging.getLogger(__name__)


def detect_doc_type(filename: str) -> DocType:
    """Fallback detection when the uploader doesn't pick a category."""
    lower = filename.lower()
    if "brd" in lower or "requirement" in lower:
        return DocType.brd
    if "meeting" in lower or "transcript" in lower or "standup" in lower:
        return DocType.transcript
    if "change" in lower or lower.startswith("cr") or "-cr-" in lower:
        return DocType.change_request
    return DocType.other


def _extract_text(content: bytes, mime: str | None, filename: str) -> str:
    if filename.lower().endswith(".pdf") or (mime and "pdf" in mime):
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(content))
        if len(reader.pages) > settings.max_pdf_pages:
            raise HTTPException(status_code=400, detail=f"PDF exceeds {settings.max_pdf_pages} pages")
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No extractable text (scanned PDFs are not supported)")
        return text
    try:
        return content.decode("utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Could not read document as text")


async def process_document(document_id: uuid.UUID, content: bytes, mime: str | None, filename: str) -> None:
    """Background task: parse → LLM extract → persist. Opens its own session."""
    async with AsyncSessionLocal() as db:
        doc = await db.get(Document, document_id)
        if not doc:
            return
        try:
            doc.status = DocStatus.parsing
            await db.commit()
            text = _extract_text(content, mime, filename)

            doc.status = DocStatus.analyzing
            await db.commit()
            raw = await client.complete(
                feature=LLMFeature.document,
                messages=prompts.document_messages(doc.doc_type.value, text),
                model=settings.llm_model_analysis,
                project_id=doc.project_id,
                temperature=0.1,
                json_mode=True,
            )
            try:
                extraction = json.loads(raw)
            except json.JSONDecodeError:
                extraction = {"summary": raw}

            db.add(DocumentExtraction(
                document_id=doc.id,
                extraction=extraction,
                summary=extraction.get("summary"),
                model=settings.llm_model_analysis,
            ))
            doc.status = DocStatus.complete
            await db.commit()

            from app.queue import get_arq_pool
            pool = await get_arq_pool()
            await pool.enqueue_job("sync_requirement_catalog", str(doc.project_id))
            await pool.enqueue_job("sync_decision_log", str(doc.project_id))
            await pool.enqueue_job("sync_action_items", str(doc.project_id))
            await pool.enqueue_job("scan_project_risks", str(doc.project_id))
        except HTTPException as exc:
            await db.rollback()
            doc.status = DocStatus.error
            doc.error = exc.detail
            await db.commit()
        except Exception as exc:  # noqa: BLE001
            await db.rollback()
            doc.status = DocStatus.error
            doc.error = str(exc)[:1000]
            await db.commit()
            logger.exception("Document processing failed for %s", document_id)
