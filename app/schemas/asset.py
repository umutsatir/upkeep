# OWNER: MEMBER-2
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.asset import AssetStatus


class AssetCreate(BaseModel):
    model_config = {"protected_namespaces": ()}
    name: str
    asset_tag: str
    category: str
    location: Optional[str] = None
    assigned_to: Optional[str] = None
    purchase_date: Optional[datetime] = None
    warranty_expires_at: Optional[datetime] = None
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    notes: str = ""


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[AssetStatus] = None
    warranty_expires_at: Optional[datetime] = None
    notes: Optional[str] = None


class AssetResponse(BaseModel):
    id: str
    name: str
    asset_tag: str
    category: str
    status: AssetStatus
    location: Optional[str]
    assigned_to: Optional[str]
    purchase_date: Optional[datetime]
    warranty_expires_at: Optional[datetime]
    model_number: Optional[str]
    serial_number: Optional[str]
    notes: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True, "protected_namespaces": ()}
