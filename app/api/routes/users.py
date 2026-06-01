# OWNER: MEMBER-1
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService

router = APIRouter()


def _service(db: AsyncIOMotorDatabase = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(payload: UserCreate, svc: UserService = Depends(_service)):
    """TODO (MEMBER-1): implement via UserService.create_user."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 100, svc: UserService = Depends(_service)):
    """TODO (MEMBER-1)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, svc: UserService = Depends(_service)):
    """TODO (MEMBER-1)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, payload: UserUpdate, svc: UserService = Depends(_service)):
    """TODO (MEMBER-1)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str, svc: UserService = Depends(_service)):
    """TODO (MEMBER-1)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")
