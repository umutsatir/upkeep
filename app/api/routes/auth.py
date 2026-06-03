# OWNER: MEMBER-1
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.database import get_db
from app.core.exceptions import DuplicateError
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: UserCreate, db=Depends(get_db)):
    """Register a new user without requiring authentication."""
    svc = UserService(db)
    try:
        user = await svc.create_user(payload)
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return UserResponse(**user.model_dump())


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db=Depends(get_db)):
    svc = UserService(db)
    token = await svc.authenticate(payload.email, payload.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid email or password",
        )
    return TokenResponse(access_token=token)
