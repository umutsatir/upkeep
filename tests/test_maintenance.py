# OWNER: MEMBER-3
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest
from bson import ObjectId

from app.models.maintenance import MaintenanceSchedule, TriggerType
from app.services.maintenance_strategies import TimeBasedStrategy, UsageBasedStrategy
from app.schemas.maintenance import MaintenanceScheduleCreate


@pytest.mark.asyncio
async def test_time_based_strategy_is_due():
    schedule = MaintenanceSchedule(
        asset_id=ObjectId(),
        title='Inspect filter',
        description='Monthly filter inspection',
        trigger_type=TriggerType.TIME_BASED,
        interval_days=30,
        next_due_at=datetime.now(timezone.utc) - timedelta(days=1),
    )

    assert TimeBasedStrategy().is_due(schedule, now=datetime.now(timezone.utc))


@pytest.mark.asyncio
async def test_usage_based_strategy_is_due():
    schedule = MaintenanceSchedule(
        asset_id=ObjectId(),
        title='Oil change',
        description='Replace oil after threshold',
        trigger_type=TriggerType.USAGE_BASED,
        usage_threshold_hours=100.0,
        current_usage_hours=120.0,
    )

    assert UsageBasedStrategy().is_due(schedule, now=datetime.now(timezone.utc), current_usage_hours=schedule.current_usage_hours)


@pytest.mark.asyncio
async def test_list_maintenance_schedules_route(client):
    sample_schedule = MaintenanceSchedule(
        asset_id=ObjectId(),
        title='Inspect filter',
        description='Monthly filter inspection',
        trigger_type=TriggerType.TIME_BASED,
        interval_days=30,
    )

    with patch('app.api.routes.maintenance.MaintenanceService.list', new=AsyncMock(return_value=[sample_schedule])):
        resp = await client.get('/api/v1/maintenance')

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]['title'] == sample_schedule.title
    assert data[0]['trigger_type'] == 'time_based'


@pytest.mark.asyncio
async def test_evaluate_due_schedules_route(client):
    with patch(
        'app.api.routes.maintenance.MaintenanceService.evaluate_due_schedules',
        new=AsyncMock(return_value=['60a7f3d83e3f2b5b2c9f0f1e']),
    ):
        resp = await client.post('/api/v1/maintenance/evaluate')

    assert resp.status_code == 200
    assert resp.json() == {'generated_work_orders': ['60a7f3d83e3f2b5b2c9f0f1e']}
