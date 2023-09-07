from fastapi import APIRouter
from pydantic import EmailStr

from ...models.user import User
from ..schemas.user import UserInfo

router = APIRouter()


@router.get("/users/{email}", tags=["User"], response_model=UserInfo)
async def get_user(email: EmailStr) -> UserInfo:
    """Get user by email."""
    user = await User.load_from_database(email=email)
    return user.asdict()
