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


# ------------------------------------------------------------------
# CRUD
# ------------------------------------------------------------------


@router.post("/", response_model=InventoryItemResponse, status_code=201)
async def create_item(
    payload: InventoryItemCreate, svc: InventoryService = Depends(_service)
):
    """Create a new inventory item."""
    try:
        item = await svc.create(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return _to_response(item)


@router.get("/", response_model=list[InventoryItemResponse])
async def list_items(
    skip: int = 0,
    limit: int = 100,
    svc: InventoryService = Depends(_service),
):
    """List all inventory items (paginated)."""
    items = await svc.list(skip=skip, limit=limit)
    return [_to_response(i) for i in items]


@router.get("/low-stock", response_model=list[InventoryItemResponse])
async def list_low_stock(svc: InventoryService = Depends(_service)):
    """Return items where quantity_on_hand <= low_stock_threshold."""
    items = await svc.list_low_stock()
    return [_to_response(i) for i in items]


@router.get("/{item_id}", response_model=InventoryItemResponse)
async def get_item(item_id: str, svc: InventoryService = Depends(_service)):
    """Get a single inventory item by ID."""
    item = await svc.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return _to_response(item)


@router.patch("/{item_id}", response_model=InventoryItemResponse)
async def update_item(
    item_id: str,
    payload: InventoryItemUpdate,
    svc: InventoryService = Depends(_service),
):
    """Partially update an inventory item."""
    item = await svc.update(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return _to_response(item)


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: str, svc: InventoryService = Depends(_service)):
    """Delete an inventory item."""
    deleted = await svc.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Inventory item not found")


# ------------------------------------------------------------------
# Stock operations
# ------------------------------------------------------------------


@router.post("/{item_id}/consume", response_model=InventoryItemResponse)
async def consume_stock(
    item_id: str,
    adjustment: StockAdjustment,
    svc: InventoryService = Depends(_service),
):
    """Deduct stock and log consumption against a work order."""
    try:
        item = await svc.consume(item_id, adjustment)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return _to_response(item)


@router.post("/{item_id}/restock", response_model=InventoryItemResponse)
async def restock(
    item_id: str,
    adjustment: StockAdjustment,
    svc: InventoryService = Depends(_service),
):
    """Add stock and record the restock event."""
    try:
        item = await svc.restock(item_id, adjustment)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return _to_response(item)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _to_response(item) -> dict:
    """Convert an InventoryItem domain entity to a response dict."""
    return {
        "id": str(item.id),
        "name": item.name,
        "sku": item.sku,
        "category": item.category,
        "quantity_on_hand": item.quantity_on_hand,
        "low_stock_threshold": item.low_stock_threshold,
        "unit_cost": item.unit_cost,
        "unit": item.unit,
        "supplier": item.supplier,
        "location": item.location,
        "notes": item.notes,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }
