# OWNER: MEMBER-3
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Optional

from app.models.maintenance import MaintenanceSchedule, TriggerType


class MaintenanceTriggerStrategy(ABC):
    @abstractmethod
    def is_due(
        self,
        schedule: MaintenanceSchedule,
        *,
        now: datetime,
        current_usage_hours: Optional[float] = None,
    ) -> bool:
        ...


class TimeBasedStrategy(MaintenanceTriggerStrategy):
    def is_due(
        self,
        schedule: MaintenanceSchedule,
        *,
        now: datetime,
        current_usage_hours: Optional[float] = None,
    ) -> bool:
        if schedule.next_due_at is None:
            return False
        # Ensure both datetimes are timezone-aware for comparison
        next_due = schedule.next_due_at
        if next_due.tzinfo is None:
            next_due = next_due.replace(tzinfo=timezone.utc)
        return next_due <= now
            
        due = schedule.next_due_at
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
            
        current_time = now
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)
            
        return due <= current_time


class UsageBasedStrategy(MaintenanceTriggerStrategy):
    def is_due(
        self,
        schedule: MaintenanceSchedule,
        *,
        now: datetime,
        current_usage_hours: Optional[float] = None,
    ) -> bool:
        if schedule.usage_threshold_hours is None:
            return False
        if current_usage_hours is None:
            return False
        return current_usage_hours >= schedule.usage_threshold_hours


def get_trigger_strategy(trigger_type: TriggerType) -> MaintenanceTriggerStrategy:
    if trigger_type == TriggerType.TIME_BASED:
        return TimeBasedStrategy()
    if trigger_type == TriggerType.USAGE_BASED:
        return UsageBasedStrategy()
    raise ValueError(f"Unknown trigger type: {trigger_type}")
