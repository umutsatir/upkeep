# OWNER: MEMBER-1
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db
from app.core.deps import get_current_user, require_admin
from app.core.exceptions import DuplicateError
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


def _svc(db: AsyncIOMotorDatabase = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return UserResponse(**current_user.model_dump())


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(
    payload: UserCreate,
    svc: UserService = Depends(_svc),
    _: User = Depends(require_admin),
):
    try:
        user = await svc.create_user(payload)
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return UserResponse(**user.model_dump())


@router.get("", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    svc: UserService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    users = await svc.list_users(skip=skip, limit=limit)
    return [UserResponse(**u.model_dump()) for u in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    svc: UserService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    user = await svc.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return UserResponse(**user.model_dump())


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    payload: UserUpdate,
    svc: UserService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    user = await svc.update_user(user_id, payload)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return UserResponse(**user.model_dump())


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str,
    svc: UserService = Depends(_svc),
    _: User = Depends(require_admin),
):
    deleted = await svc.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="user not found")
