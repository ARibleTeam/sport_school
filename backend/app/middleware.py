from fastapi import Depends, HTTPException
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_403_FORBIDDEN
from typing import Callable, Awaitable

from app.database import async_session_maker
from app.user.models import User
from app.user.schemas import UserSchema

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"

async def get_current_user(security_scopes: SecurityScopes, request: Request) -> UserSchema:
    """
        Функция для получения текущего пользователя из токена JWT.

        Args:
            security_scopes (SecurityScopes): Области безопасности (security scopes).
            request (Request): Объект запроса FastAPI.

        Returns:
            UserSchema: Схема пользователя, полученная из токена.
    """

    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")
    
    if token.startswith("Bearer "):
        token = token[7:]
    else:
         raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid authentication scheme")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid token")

    async with async_session_maker() as session:
        user = await session.get(User, int(user_id))
        if user is None:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User not found")

        return UserSchema(id=user.id, name=user.full_name, isAdmin= await User.is_admin(user_id=user.id), isAthlete= await User.is_athlete(user_id=user.id))

