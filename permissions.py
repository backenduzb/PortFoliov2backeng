from fastapi import Request, HTTPException
from authentication.jwt import verify_token
from models.user import User

async def get_current_user_cookie(request: Request):

    token = request.cookies.get('access_token')

    if not token:
        raise HTTPException(status_code=401, detail="Token topilmadi.")

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token noto‘g‘ri yoki eskirgan.")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Username token ichida yo‘q.")

    user = await User.get_or_none(username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi.")

    return user