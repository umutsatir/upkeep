# OWNER: MEMBER-1
# Shared pytest fixtures
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock

from app.main import app
from app.core import database as db_module
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User, Role


def _mock_user() -> User:
    return User(
        full_name="Test User",
        email="test@example.com",
        hashed_password="hashed",
        role=Role.ADMIN,
    )


def _override_get_current_user() -> User:
    return _mock_user()


def _override_get_db():
    """Return a MagicMock so route dependencies that call get_db() don't
    blow up. Individual tests that need real DB behaviour should mock at the
    service/repository level."""
    return MagicMock()


@pytest_asyncio.fixture
async def client(monkeypatch):
    """ASGI test client. DB and auth dependencies are overridden so tests
    are fully self-contained — no running MongoDB required."""

    async def fake_connect():
        pass

    async def fake_close():
        pass

    monkeypatch.setattr(db_module, "connect_db", fake_connect)
    monkeypatch.setattr(db_module, "close_db", fake_close)

    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_current_user] = _override_get_current_user

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def mock_user() -> User:
    return _mock_user()
