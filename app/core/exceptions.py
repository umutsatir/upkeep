# OWNER: MEMBER-1
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.work_order import WorkOrderStatus


class InvalidTransitionError(Exception):
    def __init__(self, current: WorkOrderStatus, requested: WorkOrderStatus) -> None:
        self.current = current
        self.requested = requested
        super().__init__(f"cannot transition from '{current}' to '{requested}'")


class NotFoundError(Exception):
    def __init__(self, entity: str, entity_id: str) -> None:
        super().__init__(f"{entity} '{entity_id}' not found")


class DuplicateError(Exception):
    def __init__(self, field: str, value: str) -> None:
        super().__init__(f"a record with {field}='{value}' already exists")
