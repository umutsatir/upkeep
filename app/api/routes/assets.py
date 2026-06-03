# OWNER: MEMBER-2
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.exceptions import DuplicateError, NotFoundError
from app.models.user import User
from app.models.asset import RepairRecord
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse, RepairRecordResponse
from app.services.asset_service import AssetService

router = APIRouter()


def _svc(db: AsyncIOMotorDatabase = Depends(get_db)) -> AssetService:
    return AssetService(db)


@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    payload: AssetCreate,
    svc: AssetService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    """Create a new asset."""
    try:
        asset = await svc.create(payload)
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return AssetResponse.model_validate(asset)


@router.get("/expiring-warranties", response_model=list[AssetResponse])
async def list_expiring_warranties(
    days: int = 30,
    svc: AssetService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    """List assets whose warranties are expiring within the specified days."""
    assets = await svc.list_expiring_warranties(days_ahead=days)
    return [AssetResponse.model_validate(a) for a in assets]


@router.get("/", response_model=list[AssetResponse])
async def list_assets(
    skip: int = 0,
    limit: int = 100,
    svc: AssetService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    """List all assets with pagination."""
    assets = await svc.list(skip=skip, limit=limit)
    return [AssetResponse.model_validate(a) for a in assets]


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    svc: AssetService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    """Get an asset by ID."""
    asset = await svc.get(asset_id)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return AssetResponse.model_validate(asset)


@router.patch("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: str,
    payload: AssetUpdate,
    svc: AssetService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    """Update an asset."""
    asset = await svc.update(asset_id, payload)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return AssetResponse.model_validate(asset)


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: str,
    svc: AssetService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    """Delete an asset."""
    deleted = await svc.delete(asset_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")


@router.post("/{asset_id}/repair-record", response_model=AssetResponse)
async def add_repair_record(
    asset_id: str,
    payload: RepairRecordResponse,
    svc: AssetService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    """Manually add a repair record to an asset."""
    try:
        record = RepairRecord(**payload.model_dump())
        asset = await svc.add_repair_record(asset_id, record)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return AssetResponse.model_validate(asset)


@router.post("/{asset_id}/activate", response_model=AssetResponse)
async def activate_asset(
    asset_id: str,
    svc: AssetService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    """Transition asset to ACTIVE status."""
    try:
        asset = await svc.activate(asset_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return AssetResponse.model_validate(asset)


@router.post("/{asset_id}/decommission", response_model=AssetResponse)
async def decommission_asset(
    asset_id: str,
    svc: AssetService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    """Transition asset to DECOMMISSIONED status."""
    try:
        asset = await svc.decommission(asset_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return AssetResponse.model_validate(asset)


@router.post("/{asset_id}/send-to-maintenance", response_model=AssetResponse)
async def send_asset_to_maintenance(
    asset_id: str,
    svc: AssetService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    """Transition asset to UNDER_MAINTENANCE status."""
    try:
        asset = await svc.send_to_maintenance(asset_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return AssetResponse.model_validate(asset)
