# OWNER: MEMBER-2
# TODO (MEMBER-2): Add tests for:
# - Asset creation and unique asset_tag enforcement
# - Status lifecycle transitions
# - Warranty expiry check
# - Repair history append
# - list_expiring_warranties query
import pytest


@pytest.mark.skip(reason="TODO: implement after AssetService is built")
async def test_create_asset():
    pass


@pytest.mark.skip(reason="TODO: implement after AssetService is built")
async def test_duplicate_asset_tag_rejected():
    pass
