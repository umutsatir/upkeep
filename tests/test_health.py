# OWNER: MEMBER-1
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_health_returns_ok(client):
    """Health endpoint must return 200 {"status": "ok"} when Mongo responds."""
    fake_db = AsyncMock()
    fake_db.command = AsyncMock(return_value={"ok": 1})

    with patch("app.main.get_db", return_value=fake_db):
        resp = await client.get("/health")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
