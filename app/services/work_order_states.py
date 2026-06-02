# OWNER: MEMBER-1
"""
State pattern for WorkOrder lifecycle.

Valid transitions:
    OPEN → ASSIGNED → IN_PROGRESS → COMPLETED → CLOSED
    Any non-terminal state → CANCELLED
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from app.core.exceptions import InvalidTransitionError
from app.models.work_order import WorkOrderStatus

if TYPE_CHECKING:
    from app.models.work_order import WorkOrder


class WorkOrderState(ABC):
    @abstractmethod
    def allowed_transitions(self) -> set:
        ...

    def transition(
        self,
        wo: WorkOrder,
        new_status: WorkOrderStatus,
        assigned_to: Optional[str] = None,
    ) -> None:
        if new_status not in self.allowed_transitions():
            raise InvalidTransitionError(wo.status, new_status)
        wo.status = new_status
        if assigned_to is not None:
            wo.assigned_to = assigned_to
        if new_status == WorkOrderStatus.COMPLETED:
            wo.completed_at = datetime.now(timezone.utc)


class OpenState(WorkOrderState):
    def allowed_transitions(self) -> set:
        return {WorkOrderStatus.ASSIGNED, WorkOrderStatus.CANCELLED}


class AssignedState(WorkOrderState):
    def allowed_transitions(self) -> set:
        return {WorkOrderStatus.IN_PROGRESS, WorkOrderStatus.CANCELLED}


class InProgressState(WorkOrderState):
    def allowed_transitions(self) -> set:
        return {WorkOrderStatus.COMPLETED, WorkOrderStatus.CANCELLED}


class CompletedState(WorkOrderState):
    def allowed_transitions(self) -> set:
        return {WorkOrderStatus.CLOSED}


class ClosedState(WorkOrderState):
    def allowed_transitions(self) -> set:
        return set()


class CancelledState(WorkOrderState):
    def allowed_transitions(self) -> set:
        return set()


_STATE_MAP: dict = {
    WorkOrderStatus.OPEN:        OpenState(),
    WorkOrderStatus.ASSIGNED:    AssignedState(),
    WorkOrderStatus.IN_PROGRESS: InProgressState(),
    WorkOrderStatus.COMPLETED:   CompletedState(),
    WorkOrderStatus.CLOSED:      ClosedState(),
    WorkOrderStatus.CANCELLED:   CancelledState(),
}


def get_state(status: WorkOrderStatus) -> WorkOrderState:
    return _STATE_MAP[status]
