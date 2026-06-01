# OWNER: MEMBER-4
from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class InventoryItemCreate(BaseModel):
    name: str
    sku: str
    category: str
    quantity_on_hand: int = 0
    low_stock_threshold: int = 5
    unit_cost: float = 0.0
    unit: str = "pcs"
    supplier: Optional[str] = None
    location: Optional[str] = None
    notes: str = ""


class InventoryItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity_on_hand: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    unit_cost: Optional[float] = None
    unit: Optional[str] = None
    supplier: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class StockAdjustment(BaseModel):
    """Used for consume / restock endpoints."""

    quantity: int
    work_order_id: Optional[str] = None  # required when consuming
    notes: str = ""


class InventoryItemResponse(BaseModel):
    id: str
    name: str
    sku: str
    category: str
    quantity_on_hand: int
    low_stock_threshold: int
    unit_cost: float
    unit: str
    supplier: Optional[str]
    location: Optional[str]
    notes: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
