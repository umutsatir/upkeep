# OWNER: MEMBER-2
"""
Tests are split into two layers (mirrors MEMBER-1's work_order test structure):
  1. Unit tests for model logic (pure Python, no DB, always fast).
  2. API tests for the endpoints (service is mocked at the dependency level).
"""
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch
from bson import ObjectId

from app.core.exceptions import DuplicateError, NotFoundError
from app.models.asset import Asset, AssetStatus, RepairRecord
from app.services.asset_service import AssetService


# ── helpers ────────────────────────────────────────────────────────────────

def _asset(**kwargs) -> Asset:
    defaults = dict(
        name="Main HVAC",
        asset_tag="HVAC-001",
        category="Electrical",
    )
    defaults.update(kwargs)
    return Asset(**defaults)


# ── Unit tests: model & business logic ─────────────────────────────────────

class TestAssetModel:
    def test_default_status_is_active(self):
        asset = _asset()
        assert asset.status == AssetStatus.ACTIVE

    def test_repair_history_starts_empty(self):
        asset = _asset()
        assert asset.repair_history == []

    def test_can_append_repair_record(self):
        asset = _asset()
        record = RepairRecord(
            date=datetime.now(timezone.utc),
            description="Replaced filter",
            cost=150.0,
            work_order_id=str(ObjectId()),
        )
        asset.repair_history.append(record)
        assert len(asset.repair_history) == 1
        assert asset.repair_history[0].cost == 150.0


class TestWarrantyLogic:
    def test_no_warranty_is_not_expired(self):
        svc = AssetService.__new__(AssetService)  # skip __init__
        asset = _asset(warranty_expires_at=None)
        assert svc.is_warranty_expired(asset) is False

    def test_future_warranty_is_not_expired(self):
        svc = AssetService.__new__(AssetService)
        future = datetime.now(timezone.utc) + timedelta(days=30)
        asset = _asset(warranty_expires_at=future)
        assert svc.is_warranty_expired(asset) is False

    def test_past_warranty_is_expired(self):
        svc = AssetService.__new__(AssetService)
        past = datetime.now(timezone.utc) - timedelta(days=1)
        asset = _asset(warranty_expires_at=past)
        assert svc.is_warranty_expired(asset) is True


class TestLifecycleTransitions:
    def test_status_can_be_set_to_under_maintenance(self):
        asset = _asset()
        asset.status = AssetStatus.UNDER_MAINTENANCE
        assert asset.status == AssetStatus.UNDER_MAINTENANCE

    def test_status_can_be_set_to_decommissioned(self):
        asset = _asset()
        asset.status = AssetStatus.DECOMMISSIONED
        assert asset.status == AssetStatus.DECOMMISSIONED

    def test_status_can_be_set_to_inactive(self):
        asset = _asset()
        asset.status = AssetStatus.INACTIVE
        assert asset.status == AssetStatus.INACTIVE


# ── API endpoint tests (service mocked) ────────────────────────────────────

@pytest.fixture
def sample_asset():
    return _asset()


@pytest.mark.asyncio
async def test_list_assets_empty(client):
    with patch(
        "app.api.routes.assets.AssetService.list",
        new=AsyncMock(return_value=[]),
    ):
        resp = await client.get("/api/v1/assets")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_assets_returns_items(client, sample_asset):
    with patch(
        "app.api.routes.assets.AssetService.list",
        new=AsyncMock(return_value=[sample_asset]),
    ):
        resp = await client.get("/api/v1/assets")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_asset.name
    assert data[0]["status"] == "active"


@pytest.mark.asyncio
async def test_get_asset_not_found(client):
    with patch(
        "app.api.routes.assets.AssetService.get",
        new=AsyncMock(return_value=None),
    ):
        resp = await client.get(f"/api/v1/assets/{ObjectId()}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_asset_found(client, sample_asset):
    with patch(
        "app.api.routes.assets.AssetService.get",
        new=AsyncMock(return_value=sample_asset),
    ):
        resp = await client.get(f"/api/v1/assets/{sample_asset.id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == sample_asset.id


@pytest.mark.asyncio
async def test_create_asset(client, sample_asset):
    with patch(
        "app.api.routes.assets.AssetService.create",
        new=AsyncMock(return_value=sample_asset),
    ):
        resp = await client.post("/api/v1/assets", json={
            "name": "Main HVAC",
            "asset_tag": "HVAC-001",
            "category": "Electrical",
        })
    assert resp.status_code == 201
    assert resp.json()["asset_tag"] == "HVAC-001"


@pytest.mark.asyncio
async def test_create_asset_duplicate_tag_returns_409(client):
    with patch(
        "app.api.routes.assets.AssetService.create",
        new=AsyncMock(side_effect=DuplicateError("asset_tag", "HVAC-001")),
    ):
        resp = await client.post("/api/v1/assets", json={
            "name": "Duplicate",
            "asset_tag": "HVAC-001",
            "category": "Electrical",
        })
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_update_asset_not_found(client):
    with patch(
        "app.api.routes.assets.AssetService.update",
        new=AsyncMock(return_value=None),
    ):
        resp = await client.patch(
            f"/api/v1/assets/{ObjectId()}",
            json={"name": "Updated"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_asset_ok(client, sample_asset):
    with patch(
        "app.api.routes.assets.AssetService.update",
        new=AsyncMock(return_value=sample_asset),
    ):
        resp = await client.patch(
            f"/api/v1/assets/{sample_asset.id}",
            json={"name": "Updated HVAC"},
        )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_delete_asset_not_found(client):
    with patch(
        "app.api.routes.assets.AssetService.delete",
        new=AsyncMock(return_value=False),
    ):
        resp = await client.delete(f"/api/v1/assets/{ObjectId()}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_asset_ok(client, sample_asset):
    with patch(
        "app.api.routes.assets.AssetService.delete",
        new=AsyncMock(return_value=True),
    ):
        resp = await client.delete(f"/api/v1/assets/{sample_asset.id}")
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_activate_asset(client, sample_asset):
    sample_asset.status = AssetStatus.ACTIVE
    with patch(
        "app.api.routes.assets.AssetService.activate",
        new=AsyncMock(return_value=sample_asset),
    ):
        resp = await client.post(f"/api/v1/assets/{sample_asset.id}/activate")
    assert resp.status_code == 200
    assert resp.json()["status"] == "active"


@pytest.mark.asyncio
async def test_activate_asset_not_found(client):
    with patch(
        "app.api.routes.assets.AssetService.activate",
        new=AsyncMock(side_effect=NotFoundError("Asset", str(ObjectId()))),
    ):
        resp = await client.post(f"/api/v1/assets/{ObjectId()}/activate")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_decommission_asset(client, sample_asset):
    sample_asset.status = AssetStatus.DECOMMISSIONED
    with patch(
        "app.api.routes.assets.AssetService.decommission",
        new=AsyncMock(return_value=sample_asset),
    ):
        resp = await client.post(f"/api/v1/assets/{sample_asset.id}/decommission")
    assert resp.status_code == 200
    assert resp.json()["status"] == "decommissioned"

