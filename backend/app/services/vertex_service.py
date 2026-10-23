import os
import hashlib
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
import google.auth

from app.config import settings

logger = logging.getLogger("soar-api.vertex")

_CLIENT: Optional[genai.Client] = None
_CLIENT_INITIALIZED = False


def get_vertex_client() -> Optional[genai.Client]:
    """
    Initializes and returns the Google Cloud Vertex AI GenAI Client.
    Uses Application Default Credentials (ADC) from the GCP Virtual Machine
    (Service Account with roles/aiplatform.user) to route requests and bill directly
    to Google Cloud Vertex AI.
    """
    global _CLIENT, _CLIENT_INITIALIZED
    if _CLIENT_INITIALIZED:
        return _CLIENT

    # 1. Resolve credentials and project via Application Default Credentials (ADC)
    credentials = None
    detected_project = None
    try:
        credentials, detected_project = google.auth.default()
    except Exception as e:
        logger.debug(f"ADC lookup: {e}")

    # Determine GCP project (configured in settings, or auto-detected by ADC from VM metadata)
    project = settings.GOOGLE_CLOUD_PROJECT or detected_project or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT_ID")
    location = settings.GOOGLE_CLOUD_LOCATION or "us-central1"

    try:
        # vertexai=True routes calls through Google Cloud Vertex AI
        _CLIENT = genai.Client(
            vertexai=True,
            project=project,
            location=location,
            credentials=credentials
        )
        # Patch upstream google-genai 2.33.0 aclose AttributeError if present
        if hasattr(_CLIENT, "_api_client") and not hasattr(_CLIENT._api_client, "_async_httpx_client"):
            _CLIENT._api_client._async_httpx_client = None

        _CLIENT_INITIALIZED = True
        logger.info(f"Google Cloud Vertex AI Client active via ADC (Project: {project}, Region: {location})")
        return _CLIENT
    except Exception as e:
        logger.warning(
            f"Google Cloud Vertex AI client initialization pending or failed: {e}. "
            "On GCP VM, ensure roles/aiplatform.user is attached to the VM Service Account."
        )
        _CLIENT_INITIALIZED = True
        _CLIENT = None
        return None


def generate_embedding(text: str) -> List[float]:
    """
    Generates text embedding using Google Cloud Vertex AI text-embedding-004.
    Dimension: 768.
    All calls are charged to the Google Cloud Project's Vertex AI quota.
    Falls back to deterministic normalized vector if offline/no GCP connection.
    """
    client = get_vertex_client()
    if client:
        try:
            response = client.models.embed_content(
                model=settings.EMBED_MODEL,
                contents=text,
                config=types.EmbedContentConfig(
                    output_dimensionality=settings.EMBED_DIM
                )
            )
            if response.embeddings and len(response.embeddings) > 0:
                values = response.embeddings[0].values
                if len(values) == settings.EMBED_DIM:
                    return list(values)
        except Exception as e:
            logger.warning(f"Vertex AI embedding API call failed: {e}. Using deterministic fallback.")

    # Offline / local development fallback
    return _generate_fallback_embedding(text, dim=settings.EMBED_DIM)


def _generate_fallback_embedding(text: str, dim: int = 768) -> List[float]:
    """
    Generates a normalized deterministic vector for testing when Vertex AI credentials
    are not yet active on the local machine.
    """
    import math
    vector = []
    for i in range(dim):
        h = hashlib.sha256(f"{text}_{i}".encode("utf-8")).hexdigest()
        val = (int(h[:8], 16) / 0xFFFFFFFF) * 2.0 - 1.0
        vector.append(val)

    norm = math.sqrt(sum(x * x for x in vector)) or 1.0
    return [round(x / norm, 6) for x in vector]
