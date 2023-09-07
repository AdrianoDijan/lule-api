from uuid import UUID

from pydantic import BaseModel, EmailStr

from ...constants import UserRole
from .course import CourseInfo


class UserCreationRequest(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.STUDENT


class UserCreationResponse(BaseModel):
    user_id: UUID


class UserInfo(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    courses: list[CourseInfo]
