# OWNER: MEMBER-1
# TODO (MEMBER-1): Add tests for:
# - WorkOrder creation with valid payload
# - Status transitions (valid and invalid)
# - State pattern: each state only allows its valid next states
# - 404 on get/update/delete for unknown id
# - Integration: completion deducts inventory (mock InventoryService)
import pytest


@pytest.mark.skip(reason="TODO: implement after WorkOrderService is built")
async def test_create_work_order():
    pass


@pytest.mark.skip(reason="TODO: implement after WorkOrderService is built")
async def test_invalid_status_transition_raises_error():
    pass
