# OWNER: MEMBER-1
"""
Tests are split into two layers:
  1. Unit tests for the State pattern (pure Python, no DB, always fast).
  2. API tests for the endpoints (service is mocked at the dependency level).
"""
import pytest
from unittest.mock import AsyncMock, patch
from bson import ObjectId

from app.core.exceptions import InvalidTransitionError
from app.models.work_order import WorkOrder, WorkOrderStatus, WorkOrderPriority
from app.services.work_order_states import (
    get_state,
    OpenState, AssignedState, InProgressState, CompletedState,
    ClosedState, CancelledState,
)


# ── helpers ────────────────────────────────────────────────────────────────

def _wo(**kwargs) -> WorkOrder:
    defaults = dict(
        title="Fix HVAC",
        description="unit broken",
        asset_id=str(ObjectId()),
        created_by=str(ObjectId()),
    )
    defaults.update(kwargs)
    return WorkOrder(**defaults)


# ── State machine unit tests ───────────────────────────────────────────────

class TestOpenState:
    def test_can_assign(self):
        wo = _wo()
        user_id = str(ObjectId())
        get_state(wo.status).transition(wo, WorkOrderStatus.ASSIGNED, assigned_to=user_id)
        assert wo.status == WorkOrderStatus.ASSIGNED
        assert wo.assigned_to == user_id

    def test_can_cancel(self):
        wo = _wo()
        get_state(wo.status).transition(wo, WorkOrderStatus.CANCELLED)
        assert wo.status == WorkOrderStatus.CANCELLED

    def test_cannot_go_to_in_progress(self):
        wo = _wo()
        with pytest.raises(InvalidTransitionError):
            get_state(wo.status).transition(wo, WorkOrderStatus.IN_PROGRESS)

    def test_cannot_go_to_completed(self):
        wo = _wo()
        with pytest.raises(InvalidTransitionError):
            get_state(wo.status).transition(wo, WorkOrderStatus.COMPLETED)

    def test_cannot_go_to_closed(self):
        wo = _wo()
        with pytest.raises(InvalidTransitionError):
            get_state(wo.status).transition(wo, WorkOrderStatus.CLOSED)


class TestAssignedState:
    def _assigned_wo(self):
        wo = _wo(status=WorkOrderStatus.ASSIGNED, assigned_to=str(ObjectId()))
        return wo

    def test_can_start(self):
        wo = self._assigned_wo()
        get_state(wo.status).transition(wo, WorkOrderStatus.IN_PROGRESS)
        assert wo.status == WorkOrderStatus.IN_PROGRESS

    def test_can_cancel(self):
        wo = self._assigned_wo()
        get_state(wo.status).transition(wo, WorkOrderStatus.CANCELLED)
        assert wo.status == WorkOrderStatus.CANCELLED

    def test_cannot_jump_to_completed(self):
        wo = self._assigned_wo()
        with pytest.raises(InvalidTransitionError):
            get_state(wo.status).transition(wo, WorkOrderStatus.COMPLETED)


class TestInProgressState:
    def _in_progress_wo(self):
        return _wo(status=WorkOrderStatus.IN_PROGRESS, assigned_to=str(ObjectId()))

    def test_can_complete(self):
        wo = self._in_progress_wo()
        get_state(wo.status).transition(wo, WorkOrderStatus.COMPLETED)
        assert wo.status == WorkOrderStatus.COMPLETED
        assert wo.completed_at is not None

    def test_can_cancel(self):
        wo = self._in_progress_wo()
        get_state(wo.status).transition(wo, WorkOrderStatus.CANCELLED)
        assert wo.status == WorkOrderStatus.CANCELLED

    def test_cannot_go_back_to_assigned(self):
        wo = self._in_progress_wo()
        with pytest.raises(InvalidTransitionError):
            get_state(wo.status).transition(wo, WorkOrderStatus.ASSIGNED)


class TestCompletedState:
    def test_can_close(self):
        wo = _wo(status=WorkOrderStatus.COMPLETED)
        get_state(wo.status).transition(wo, WorkOrderStatus.CLOSED)
        assert wo.status == WorkOrderStatus.CLOSED

    def test_cannot_cancel_after_completed(self):
        wo = _wo(status=WorkOrderStatus.COMPLETED)
        with pytest.raises(InvalidTransitionError):
            get_state(wo.status).transition(wo, WorkOrderStatus.CANCELLED)


class TestTerminalStates:
    def test_closed_has_no_transitions(self):
        wo = _wo(status=WorkOrderStatus.CLOSED)
        with pytest.raises(InvalidTransitionError):
            get_state(wo.status).transition(wo, WorkOrderStatus.OPEN)

    def test_cancelled_has_no_transitions(self):
        wo = _wo(status=WorkOrderStatus.CANCELLED)
        with pytest.raises(InvalidTransitionError):
            get_state(wo.status).transition(wo, WorkOrderStatus.OPEN)


def test_invalid_transition_error_message():
    err = InvalidTransitionError(WorkOrderStatus.CLOSED, WorkOrderStatus.OPEN)
    assert "CLOSED" in str(err)
    assert "OPEN" in str(err)


# ── API endpoint tests (service mocked) ────────────────────────────────────

def _wo_dict(**kwargs) -> dict:
    wo = _wo(**kwargs)
    d = wo.model_dump()
    # Response serialises dates as strings; keep as-is for comparison keys
    return d


@pytest.fixture
def sample_wo():
    return _wo()


@pytest.mark.asyncio
async def test_list_work_orders_empty(client):
    with patch(
        "app.api.routes.work_orders.WorkOrderService.list",
        new=AsyncMock(return_value=[]),
    ):
        resp = await client.get("/api/v1/work-orders")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_work_orders_returns_items(client, sample_wo):
    with patch(
        "app.api.routes.work_orders.WorkOrderService.list",
        new=AsyncMock(return_value=[sample_wo]),
    ):
        resp = await client.get("/api/v1/work-orders")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == sample_wo.title
    assert data[0]["status"] == "open"


@pytest.mark.asyncio
async def test_get_work_order_not_found(client):
    with patch(
        "app.api.routes.work_orders.WorkOrderService.get",
        new=AsyncMock(return_value=None),
    ):
        resp = await client.get(f"/api/v1/work-orders/{ObjectId()}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_work_order_found(client, sample_wo):
    with patch(
        "app.api.routes.work_orders.WorkOrderService.get",
        new=AsyncMock(return_value=sample_wo),
    ):
        resp = await client.get(f"/api/v1/work-orders/{sample_wo.id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == sample_wo.id


@pytest.mark.asyncio
async def test_create_work_order(client, sample_wo):
    with patch(
        "app.api.routes.work_orders.WorkOrderService.create",
        new=AsyncMock(return_value=sample_wo),
    ):
        resp = await client.post("/api/v1/work-orders", json={
            "title": "Fix HVAC",
            "description": "unit broken",
            "asset_id": str(ObjectId()),
        })
    assert resp.status_code == 201
    assert resp.json()["status"] == "open"


@pytest.mark.asyncio
async def test_transition_invalid_raises_422(client, sample_wo):
    with patch(
        "app.api.routes.work_orders.WorkOrderService.transition",
        new=AsyncMock(side_effect=InvalidTransitionError(
            WorkOrderStatus.CLOSED, WorkOrderStatus.OPEN
        )),
    ):
        resp = await client.post(
            f"/api/v1/work-orders/{sample_wo.id}/transition",
            json={"new_status": "open"},
        )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_delete_work_order_not_found(client):
    with patch(
        "app.api.routes.work_orders.WorkOrderService.delete",
        new=AsyncMock(return_value=False),
    ):
        resp = await client.delete(f"/api/v1/work-orders/{ObjectId()}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_work_order_ok(client, sample_wo):
    with patch(
        "app.api.routes.work_orders.WorkOrderService.delete",
        new=AsyncMock(return_value=True),
    ):
        resp = await client.delete(f"/api/v1/work-orders/{sample_wo.id}")
    assert resp.status_code == 204
