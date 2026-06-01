# OWNER: MEMBER-2
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from app.services.asset_service import AssetService

router = APIRouter()


def _service(db: AsyncIOMotorDatabase = Depends(get_db)) -> AssetService:
    return AssetService(db)


@router.post("/", response_model=AssetResponse, status_code=201)
async def create_asset(payload: AssetCreate, svc: AssetService = Depends(_service)):
    """TODO (MEMBER-2)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/", response_model=list[AssetResponse])
async def list_assets(skip: int = 0, limit: int = 100, svc: AssetService = Depends(_service)):
    """TODO (MEMBER-2)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: str, svc: AssetService = Depends(_service)):
    """TODO (MEMBER-2)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: str, payload: AssetUpdate, svc: AssetService = Depends(_service)
):
    """TODO (MEMBER-2)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/{asset_id}", status_code=204)
async def delete_asset(asset_id: str, svc: AssetService = Depends(_service)):
    """TODO (MEMBER-2)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")
