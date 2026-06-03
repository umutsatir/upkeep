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
    """Create a new asset (stub for MEMBER-2)."""
    asset = await svc.create(payload)
    return AssetResponse(**asset.model_dump())


@router.get("/", response_model=list[AssetResponse])
async def list_assets(skip: int = 0, limit: int = 100, svc: AssetService = Depends(_service)):
    """List all assets (stub for MEMBER-2)."""
    assets = await svc.list(skip=skip, limit=limit)
    return [AssetResponse(**a.model_dump()) for a in assets]


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: str, svc: AssetService = Depends(_service)):
    """Get asset by ID (stub for MEMBER-2)."""
    asset = await svc.get(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="asset not found")
    return AssetResponse(**asset.model_dump())


@router.patch("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: str, payload: AssetUpdate, svc: AssetService = Depends(_service)
):
    """Update asset (stub for MEMBER-2)."""
    asset = await svc.update(asset_id, payload)
    if asset is None:
        raise HTTPException(status_code=404, detail="asset not found")
    return AssetResponse(**asset.model_dump())


@router.delete("/{asset_id}", status_code=204)
async def delete_asset(asset_id: str, svc: AssetService = Depends(_service)):
    """Delete asset (stub for MEMBER-2)."""
    deleted = await svc.delete(asset_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="asset not found")
