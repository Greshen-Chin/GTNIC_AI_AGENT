from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Jalur absolut ke file .env
ENV_FILE_PATH = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Security Tokens (dibaca langsung dari .env)
    INTERNAL_TOKEN: str
    DASHBOARD_API_KEY: str

    # PostgreSQL Database (dibaca langsung dari .env)
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # Wazuh Indexer (dibaca langsung dari .env)
    INDEXER_URL: str
    INDEXER_USER: str
    INDEXER_PASSWORD: Optional[str] = ""
    INDEXER_VERIFY_SSL: bool

    # Google Cloud Vertex AI (dibaca langsung dari .env)
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_CLOUD_LOCATION: str
    LLM_MODEL: str
    EMBED_MODEL: str
    EMBED_DIM: int

    # n8n Stack (dibaca langsung dari .env)
    N8N_VERSION: Optional[str] = None
    N8N_ENCRYPTION_KEY: Optional[str] = None
    CF_TUNNEL_TOKEN: Optional[str] = None

    # App Settings
    APP_NAME: str = "GTNIC SOAR-API"
    APP_ENV: str = "production"
    DEBUG: bool = False
    ALLOW_SIMULATION: bool = False


settings = Settings()
