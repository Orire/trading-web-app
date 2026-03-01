"""
Settings API endpoints
"""

from fastapi import APIRouter, HTTPException
import logging

from app.models.schemas import EtoroCredentialsCreate, EtoroCredentialsResponse
from app.services.credentials_store import CredentialsStore

logger = logging.getLogger(__name__)
router = APIRouter()
credentials_store = CredentialsStore()


@router.get("/etoro-credentials", response_model=EtoroCredentialsResponse)
async def get_etoro_credentials_status():
    """Return masked status of configured eToro credentials."""
    try:
        return credentials_store.get_etoro_credentials_status()
    except Exception as e:
        logger.error(f"Error reading eToro credentials status: {e}")
        raise HTTPException(status_code=500, detail="Failed to read credentials status")


@router.post("/etoro-credentials", response_model=EtoroCredentialsResponse)
async def save_etoro_credentials(payload: EtoroCredentialsCreate):
    """Save eToro credentials in local tenant-scoped storage."""
    try:
        return credentials_store.save_etoro_credentials(
            api_key=payload.api_key,
            api_secret=payload.api_secret,
            base_url=payload.base_url,
            environment=payload.environment,
        )
    except Exception as e:
        logger.error(f"Error saving eToro credentials: {e}")
        raise HTTPException(status_code=500, detail="Failed to save credentials")
