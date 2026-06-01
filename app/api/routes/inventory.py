# OWNER: MEMBER-4
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db
from app.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemUpdate,
    StockAdjustment,
    InventoryItemResponse,
)
from app.services.inventory_service import InventoryService

router = APIRouter()


def _service(db: AsyncIOMotorDatabase = Depends(get_db)) -> InventoryService:
    return InventoryService(db)


@router.post("/", response_model=InventoryItemResponse, status_code=201)
async def create_item(payload: InventoryItemCreate, svc: InventoryService = Depends(_service)):
    """TODO (MEMBER-4)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/", response_model=list[InventoryItemResponse])
async def list_items(
    skip: int = 0, limit: int = 100, svc: InventoryService = Depends(_service)
):
    """TODO (MEMBER-4)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/low-stock", response_model=list[InventoryItemResponse])
async def list_low_stock(svc: InventoryService = Depends(_service)):
    """TODO (MEMBER-4): Return items below their stock threshold."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{item_id}", response_model=InventoryItemResponse)
async def get_item(item_id: str, svc: InventoryService = Depends(_service)):
    """TODO (MEMBER-4)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/{item_id}", response_model=InventoryItemResponse)
async def update_item(
    item_id: str, payload: InventoryItemUpdate, svc: InventoryService = Depends(_service)
):
    """TODO (MEMBER-4)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: str, svc: InventoryService = Depends(_service)):
    """TODO (MEMBER-4)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/{item_id}/consume", response_model=InventoryItemResponse)
async def consume_stock(
    item_id: str, adjustment: StockAdjustment, svc: InventoryService = Depends(_service)
):
    """TODO (MEMBER-4): Deduct quantity and log against a work order."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/{item_id}/restock", response_model=InventoryItemResponse)
async def restock(
    item_id: str, adjustment: StockAdjustment, svc: InventoryService = Depends(_service)
):
    """TODO (MEMBER-4)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")
