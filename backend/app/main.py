import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import test_postgres_connection
from app.services.vertex_service import get_vertex_client
from app.api.internal_tools import router as internal_router
from app.api.dashboard import router as dashboard_router

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("soar-api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing GTNIC SOAR-API")
    logger.info(f"Loaded Config: LLM={settings.LLM_MODEL}, EMBED_MODEL={settings.EMBED_MODEL} ({settings.EMBED_DIM}d)")

    # Test PostgreSQL & pgvector connection
    db_ok = test_postgres_connection()
    if db_ok:
        logger.info(f"PostgreSQL connection confirmed to {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT} (DB: {settings.POSTGRES_DB})")
    else:
        logger.warning(f"PostgreSQL not reachable at {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}. Ensure Postgres container/service is running.")

    # Initialize Google Cloud Vertex AI Client
    client = get_vertex_client()
    if client:
        logger.info(f"Google Cloud Vertex AI active (Project: {settings.GOOGLE_CLOUD_PROJECT}, Region: {settings.GOOGLE_CLOUD_LOCATION})")
    else:
        logger.info("Vertex AI ready (waiting for GCP credentials in production environment)")

    yield

    logger.info("GTNIC SOAR-API shutting down gracefully.")


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Backend SOAR & AI Agent Tool Calling service for GTNIC Cybersecurity Platform. "
        "Provides read-only investigation tools for Wazuh & MITRE/OWASP RAG via Google Cloud Vertex AI, "
        "plus authenticated Dashboard REST endpoints."
    ),
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for Next.js frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(internal_router)
app.include_router(dashboard_router)


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "vertex_ai_configured": bool(settings.GOOGLE_CLOUD_PROJECT or get_vertex_client()),
        "model": settings.LLM_MODEL,
        "embed_model": settings.EMBED_MODEL,
        "embed_dim": settings.EMBED_DIM
    }


@app.get("/", tags=["System"])
def root():
    return {
        "message": "GTNIC SOAR-API is running.",
        "documentation": "/docs",
        "endpoints": {
            "internal_tools": [
                "POST /internal/tools/search_alerts_by_ip",
                "POST /internal/tools/get_login_history",
                "POST /internal/tools/mitre_owasp_rag",
                "POST /internal/agent/investigate"
            ],
            "dashboard_api": [
                "GET /api/incidents",
                "GET /api/incidents/{id}",
                "POST /api/incidents/{id}/decision",
                "GET /api/stats",
                "GET /api/benchmark"
            ]
        }
    }
