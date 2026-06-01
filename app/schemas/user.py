# OWNER: MEMBER-1
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.user import Role


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str  # plain-text; hashing happens in the service layer
    role: Role = Role.VIEWER
    department: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[Role] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    role: Role
    department: Optional[str]
    is_active: bool

    model_config = {"from_attributes": True}
