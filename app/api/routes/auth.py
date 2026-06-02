# OWNER: MEMBER-1
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.database import get_db
from app.services.user_service import UserService

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


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
