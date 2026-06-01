# OWNER: MEMBER-1
# Shared pytest fixtures
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core import database as db_module


@pytest_asyncio.fixture
async def client(monkeypatch):
    """ASGI test client with a real (or mocked) DB connection.

    For fast unit tests without Mongo, monkeypatch get_db / connect_db here.
    For integration tests, start docker-compose before running the suite.
    """
    # Override lifespan so tests don't need a real Mongo by default
    async def fake_connect():
        pass

    async def fake_close():
        pass

    monkeypatch.setattr(db_module, "connect_db", fake_connect)
    monkeypatch.setattr(db_module, "close_db", fake_close)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
