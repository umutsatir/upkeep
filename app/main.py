# OWNER: MEMBER-1
from contextlib import asynccontextmanager
from typing import AsyncIterator

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.database import connect_db, close_db, get_db
from app.api.routes import (
    auth,
    work_orders,
    assets,
    maintenance,
    inventory,
    users,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="Upkeep CMMS",
    description="Computerized Maintenance Management System",
    version="0.1.0",
    lifespan=lifespan,
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logging.getLogger("upkeep").exception("Unhandled error on %s %s", request.method, request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# --- routers ---
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(work_orders.router, prefix="/api/v1/work-orders", tags=["Work Orders"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["Assets"])
app.include_router(maintenance.router, prefix="/api/v1/maintenance", tags=["Maintenance"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["Inventory"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])


@app.get("/health", tags=["Health"])
async def health() -> dict[str, str]:
    db = get_db()
    await db.command("ping")
    return {"status": "ok"}
