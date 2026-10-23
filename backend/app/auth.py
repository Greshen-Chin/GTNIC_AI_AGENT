from typing import Optional
from fastapi import Header, HTTPException, status
from app.config import settings


def verify_internal_token(
    x_internal_token: Optional[str] = Header(None, alias="X-Internal-Token"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
) -> str:
    """
    Validates internal service-to-service token (e.g. from n8n tools to soar-api).
    Returns the token if valid, raises HTTP 401 otherwise.
    """
    token = x_internal_token
    if not token and authorization:
        if authorization.lower().startswith("bearer "):
            token = authorization[7:].strip()
        else:
            token = authorization.strip()

    if not token or token != settings.INTERNAL_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Internal-Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


def verify_dashboard_api_key(
    x_dashboard_api_key: Optional[str] = Header(None, alias="X-Dashboard-API-Key"),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
) -> str:
    """
    Validates dashboard API key from Next.js server-side route handlers.
    Checks X-Dashboard-API-Key, X-API-Key, or Bearer token against DASHBOARD_API_KEY.
    """
    key = x_dashboard_api_key or x_api_key
    if not key and authorization:
        if authorization.lower().startswith("bearer "):
            key = authorization[7:].strip()
        else:
            key = authorization.strip()

    if not key or key != settings.DASHBOARD_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing DASHBOARD_API_KEY",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return key
