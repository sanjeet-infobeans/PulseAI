from typing import Annotated

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

# Populate os.environ from .env so connector secret_ref lookups (os.environ.get)
# resolve tokens like JIRA_TOKEN_ATLAS that live in .env.
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    redis_url: str
    secret_key: str

    # Org bootstrap — seeds super admin + demo customer/project on first startup
    super_admin_email: str = "admin@infobeans.com"
    super_admin_password: str = "changeme-super"
    seed_demo_data: bool = True

    # CORS — comma-separated origins in env var (NoDecode: skip JSON pre-parsing)
    allowed_origins: Annotated[list[str], NoDecode] = ["http://localhost:3000"]

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def _parse_origins(cls, v: object) -> object:
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    # ── LLM (Groq via LiteLLM) ──────────────────────────────────────────────
    groq_api_key: str | None = None
    # LiteLLM model ids — "<provider>/<model>"
    llm_model_analysis: str = "groq/llama-3.3-70b-versatile"
    llm_model_chat: str = "groq/llama-3.1-8b-instant"
    llm_model_judge: str = "groq/llama-3.3-70b-versatile"
    llm_max_tokens: int = 2048

    # ── Supabase Storage (document uploads) ─────────────────────────────────
    supabase_url: str | None = None
    supabase_service_key: str | None = None
    supabase_bucket: str = "pulseai-documents"

    # Upload guards
    max_upload_mb: int = 15
    max_pdf_pages: int = 60


settings = Settings()
