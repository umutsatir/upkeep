# OWNER: MEMBER-4
"""
Tests for the Inventory module (MEMBER-4).

Split into three layers:
  1. Decorator pattern unit tests (pure Python, no DB)
  2. Service unit tests (repository mocked)
  3. API endpoint tests (service mocked at dependency level)
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from bson import ObjectId

from app.models.inventory import InventoryItem, ConsumptionRecord
from app.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemUpdate,
    StockAdjustment,
)
from app.services.notifiers import (
    LogNotifier,
    EmailAlertDecorator,
    SlackAlertDecorator,
    build_default_notifier,
)


# ── helpers ────────────────────────────────────────────────────────────────


def _item(**kwargs) -> InventoryItem:
    defaults = dict(
        name="Oil Filter",
        sku="FLT-001",
        category="Filters",
        quantity_on_hand=50,
        low_stock_threshold=5,
        unit_cost=12.50,
        unit="pcs",
    )
    defaults.update(kwargs)
    return InventoryItem(**defaults)


# ── Decorator pattern unit tests ───────────────────────────────────────────


class TestLogNotifier:
    def test_notify_returns_log_channel(self):
        notifier = LogNotifier()
        item = _item(quantity_on_hand=3)
        channels = notifier.notify(item)
        assert channels == ["log"]


class TestEmailAlertDecorator:
    def test_wraps_base_and_adds_email(self):
        base = LogNotifier()
        decorated = EmailAlertDecorator(base)
        item = _item(quantity_on_hand=2)
        channels = decorated.notify(item)
        assert "log" in channels
        assert "email" in channels


class TestSlackAlertDecorator:
    def test_wraps_base_and_adds_slack(self):
        base = LogNotifier()
        decorated = SlackAlertDecorator(base)
        item = _item(quantity_on_hand=1)
        channels = decorated.notify(item)
        assert "log" in channels
        assert "slack" in channels


class TestFullDecoratorChain:
    def test_all_three_channels_fire(self):
        notifier = build_default_notifier()
        item = _item(quantity_on_hand=0)
        channels = notifier.notify(item)
        assert channels == ["log", "email", "slack"]


# ── ConsumptionRecord tests ───────────────────────────────────────────────


class TestConsumptionRecord:
    def test_create_record(self):
        record = ConsumptionRecord(
            quantity=-5,
            work_order_id=str(ObjectId()),
            notes="Used for HVAC repair",
            action="consume",
        )
        assert record.quantity == -5
        assert record.action == "consume"

    def test_restock_record(self):
        record = ConsumptionRecord(
            quantity=20,
            notes="Restocked from supplier",
            action="restock",
        )
        assert record.quantity == 20
        assert record.action == "restock"


# ── InventoryItem model tests ─────────────────────────────────────────────


class TestInventoryItem:
    def test_is_low_stock_true(self):
        item = _item(quantity_on_hand=3, low_stock_threshold=5)
        assert item.is_low_stock is True

    def test_is_low_stock_at_threshold(self):
        item = _item(quantity_on_hand=5, low_stock_threshold=5)
        assert item.is_low_stock is True

    def test_is_low_stock_false(self):
        item = _item(quantity_on_hand=10, low_stock_threshold=5)
        assert item.is_low_stock is False

    def test_total_value(self):
        item = _item(quantity_on_hand=10, unit_cost=12.50)
        assert item.total_value == 125.0


# ── API endpoint tests (service mocked) ────────────────────────────────────


@pytest.fixture
def sample_item():
    return _item()


@pytest.mark.asyncio
async def test_create_item(client, sample_item):
    with patch(
        "app.services.inventory_service.InventoryService.create",
        new=AsyncMock(return_value=sample_item),
    ):
        resp = await client.post(
            "/api/v1/inventory",
            json={
                "name": "Oil Filter",
                "sku": "FLT-001",
                "category": "Filters",
            },
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Oil Filter"
    assert data["sku"] == "FLT-001"


@pytest.mark.asyncio
async def test_create_item_duplicate_sku(client):
    with patch(
        "app.services.inventory_service.InventoryService.create",
        new=AsyncMock(side_effect=ValueError("An item with SKU 'FLT-001' already exists")),
    ):
        resp = await client.post(
            "/api/v1/inventory",
            json={
                "name": "Oil Filter",
                "sku": "FLT-001",
                "category": "Filters",
            },
        )
    assert resp.status_code == 422
    assert "FLT-001" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_list_items_empty(client):
    with patch(
        "app.services.inventory_service.InventoryService.list",
        new=AsyncMock(return_value=[]),
    ):
        resp = await client.get("/api/v1/inventory")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_items_returns_items(client, sample_item):
    with patch(
        "app.services.inventory_service.InventoryService.list",
        new=AsyncMock(return_value=[sample_item]),
    ):
        resp = await client.get("/api/v1/inventory")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "Oil Filter"


@pytest.mark.asyncio
async def test_get_item_not_found(client):
    with patch(
        "app.services.inventory_service.InventoryService.get",
        new=AsyncMock(return_value=None),
    ):
        resp = await client.get(f"/api/v1/inventory/{ObjectId()}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_item_found(client, sample_item):
    with patch(
        "app.services.inventory_service.InventoryService.get",
        new=AsyncMock(return_value=sample_item),
    ):
        resp = await client.get(f"/api/v1/inventory/{sample_item.id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == sample_item.id


@pytest.mark.asyncio
async def test_update_item(client, sample_item):
    updated = _item(name="Updated Filter")
    with patch(
        "app.services.inventory_service.InventoryService.update",
        new=AsyncMock(return_value=updated),
    ):
        resp = await client.patch(
            f"/api/v1/inventory/{sample_item.id}",
            json={"name": "Updated Filter"},
        )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Filter"


@pytest.mark.asyncio
async def test_update_item_not_found(client):
    with patch(
        "app.services.inventory_service.InventoryService.update",
        new=AsyncMock(return_value=None),
    ):
        resp = await client.patch(
            f"/api/v1/inventory/{ObjectId()}",
            json={"name": "X"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_item_ok(client, sample_item):
    with patch(
        "app.services.inventory_service.InventoryService.delete",
        new=AsyncMock(return_value=True),
    ):
        resp = await client.delete(f"/api/v1/inventory/{sample_item.id}")
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_delete_item_not_found(client):
    with patch(
        "app.services.inventory_service.InventoryService.delete",
        new=AsyncMock(return_value=False),
    ):
        resp = await client.delete(f"/api/v1/inventory/{ObjectId()}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_consume_stock(client, sample_item):
    consumed = _item(quantity_on_hand=45)
    with patch(
        "app.services.inventory_service.InventoryService.consume",
        new=AsyncMock(return_value=consumed),
    ):
        resp = await client.post(
            f"/api/v1/inventory/{sample_item.id}/consume",
            json={"quantity": 5, "work_order_id": str(ObjectId()), "notes": "HVAC repair"},
        )
    assert resp.status_code == 200
    assert resp.json()["quantity_on_hand"] == 45


@pytest.mark.asyncio
async def test_consume_stock_insufficient(client, sample_item):
    with patch(
        "app.services.inventory_service.InventoryService.consume",
        new=AsyncMock(side_effect=ValueError("Insufficient stock")),
    ):
        resp = await client.post(
            f"/api/v1/inventory/{sample_item.id}/consume",
            json={"quantity": 999},
        )
    assert resp.status_code == 400
    assert "Insufficient" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_restock(client, sample_item):
    restocked = _item(quantity_on_hand=70)
    with patch(
        "app.services.inventory_service.InventoryService.restock",
        new=AsyncMock(return_value=restocked),
    ):
        resp = await client.post(
            f"/api/v1/inventory/{sample_item.id}/restock",
            json={"quantity": 20, "notes": "Weekly restock"},
        )
    assert resp.status_code == 200
    assert resp.json()["quantity_on_hand"] == 70


@pytest.mark.asyncio
async def test_list_low_stock(client):
    low_items = [_item(quantity_on_hand=2, sku="LOW-001")]
    with patch(
        "app.services.inventory_service.InventoryService.list_low_stock",
        new=AsyncMock(return_value=low_items),
    ):
        resp = await client.get("/api/v1/inventory/low-stock")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["quantity_on_hand"] == 2
