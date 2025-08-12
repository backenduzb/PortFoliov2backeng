from authentication.user_schema import UserLogoutSchema, UserLoginSchema, User_Pydantic
from tortoise.expressions import Q
from permissions import get_current_user_cookie
from fastapi import APIRouter, Depends
from models.user import User
from typing import List
from datetime import datetime
from zoneinfo import ZoneInfo


router = APIRouter(
    prefix='/user',
    tags=['user']   
)

@router.get("/search/{search_user}", response_model=List[User_Pydantic])
async def search_user(search_user: str):
    query = Q(username__icontains=search_user) | Q(first_name__icontains=search_user) | Q(last_name__icontains=search_user)
    users = await User.filter(query)
    return [await User_Pydantic.from_tortoise_orm(user) for user in users]

@router.get("/", response_model=List[User_Pydantic])
async def get_users(current_user: User = Depends(get_current_user_cookie)):
    users = User.exclude(id=current_user.id)
    return await User_Pydantic.from_queryset(users)


@router.get("/online", response_model=List[User_Pydantic])
async def get_users(current_user: User = Depends(get_current_user_cookie)):
    users = User.filter(is_online=True)
    return await User_Pydantic.from_queryset(users)

