"""Best-effort upload to Supabase Storage. If Supabase is not configured, uploads
are skipped (storage_path stays None) so the analysis pipeline still works in dev."""
import logging

from app.config import settings

logger = logging.getLogger(__name__)


def is_configured() -> bool:
    return bool(settings.supabase_url and settings.supabase_service_key)


def upload(object_path: str, content: bytes, content_type: str | None) -> str | None:
    if not is_configured():
        return None
    try:
        from supabase import create_client

        client = create_client(settings.supabase_url, settings.supabase_service_key)
        client.storage.from_(settings.supabase_bucket).upload(
            object_path,
            content,
            {"content-type": content_type or "application/octet-stream", "upsert": "true"},
        )
        return object_path
    except Exception:  # noqa: BLE001 — storage is non-critical for the POC demo
        logger.exception("Supabase upload failed for %s", object_path)
        return None


def remove(object_path: str) -> None:
    if not is_configured():
        return
    try:
        from supabase import create_client

        client = create_client(settings.supabase_url, settings.supabase_service_key)
        client.storage.from_(settings.supabase_bucket).remove([object_path])
    except Exception:  # noqa: BLE001 — best-effort cleanup
        logger.exception("Supabase remove failed for %s", object_path)
