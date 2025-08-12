from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .jwt import verify_token, create_access_token
from permissions import get_current_user_cookie
from fastapi import HTTPException, Depends
from fastapi import APIRouter, Response, Request
from models.user import User
from .user_schema import UserLoginSchema, UserLogoutSchema, UserRegisterSchema
from zoneinfo import ZoneInfo
from datetime import datetime

router = APIRouter(
    prefix='/users',
    tags=['users']
)

auth2schema = OAuth2PasswordBearer(tokenUrl="token")
@router.post("/register", response_model=UserLogoutSchema)
async def register(user: UserRegisterSchema):
    existing_user = await User.get_or_none(username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username allaqachon olingan.")

    hashed_password = User.create_password_hash(user.password)
    user_obj = await User.create(
        username=user.username,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    return await UserLogoutSchema.from_tortoise_orm(user_obj)


@router.post("/login")
async def login_json(user: UserLoginSchema, response: Response):
    user_db = await User.get_or_none(username=user.username)

    if not user_db or not user_db.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Ma'lumotlar noto‘g‘ri.")
    
    user_db.is_online = True
    user_db.last_seen = None  
    await user_db.save()
    
    token = create_access_token({"sub": user.username})
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=1000,
        samesite="None",    # Kross-domen uchun
        domain=".vercel.app" 
    )


    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.get('/me')
async def me(current_user: User = Depends(get_current_user_cookie)):
    return await UserLogoutSchema.from_tortoise_orm(current_user)

@router.get('/logout')
async def logout(response: Response, current_user: User = Depends(get_current_user_cookie)):
    current_user.is_online = False
    current_user.last_seen = datetime.now(ZoneInfo("Asia/Tashkent"))
    await current_user.save()

    response.delete_cookie('access_token')
    return {"message": "Logged out"}
