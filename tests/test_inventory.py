# OWNER: MEMBER-4
# TODO (MEMBER-4): Add tests for:
# - Item creation
# - consume() reduces quantity and logs against a WO
# - restock() increases quantity
# - consume() below threshold emits low-stock alert (mock notifier)
# - list_low_stock() returns correct items
import pytest


@pytest.mark.skip(reason="TODO: implement after InventoryService is built")
async def test_consume_reduces_stock():
    pass


@pytest.mark.skip(reason="TODO: implement after InventoryService is built")
async def test_low_stock_alert_triggered():
    pass
