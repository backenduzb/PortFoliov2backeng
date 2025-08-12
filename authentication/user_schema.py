from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from models.user import User
from typing import Optional
from zoneinfo import ZoneInfo

class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserRegisterSchema(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

class UserLogoutSchema(BaseModel):
    id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_online: bool
    last_seen: Optional[str]  
    @classmethod
    async def from_tortoise_orm(cls, user: User):
        if user.last_seen:
            last_seen_tashkent = user.last_seen.astimezone(ZoneInfo("Asia/Tashkent"))
            formatted_last_seen = last_seen_tashkent.strftime('%Y-%m-%d %H:%M')
        else:
            formatted_last_seen = None

        return cls(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_online=user.is_online,
            last_seen=formatted_last_seen
        )

class TokenData(BaseModel):
    username: str | None = None

User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password_hash",))