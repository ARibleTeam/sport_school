from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.user.schemas import UserSchema, SignUpRequest, SignInRequest
from app.user.models import User
from app.utils import verify_password, create_access_token, decode_access_token, get_password_hash, generate_refresh_token
from sqlalchemy import select, update
from fastapi.security import OAuth2PasswordBearer
from app.middleware import get_current_user
from pydantic import BaseModel


user_router = APIRouter(prefix="/users", tags=["ПОЛЬЗОВАТЕЛЬ"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@user_router.post("/signin", response_model=dict)
async def signin(request: SignInRequest):
    """
    Аутентификация пользователя и выдача токенов доступа и обновления.

    Args:
        request (SignInRequest): Данные для входа пользователя (email и пароль).
    """

    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.email == request.email))
        user = user.scalar_one_or_none()

        if not user or not verify_password(request.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Неверные учетные данные")

        access_token = create_access_token(subject=user.id)
        refresh_token = generate_refresh_token()

        user.refresh_token = refresh_token
        await session.commit()

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@user_router.post("/refresh", response_model=dict)
async def refresh_token(request: RefreshTokenRequest):
    """
    Обновление токена доступа с использованием токена обновления.

    Args:
        request (RefreshTokenRequest): Запрос, содержащий токен обновления.
    """
    refresh_token = request.refresh_token
    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.refresh_token == refresh_token))
        user = user.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

        access_token = create_access_token(subject=user.id)
        new_refresh_token = generate_refresh_token()

        user.refresh_token = new_refresh_token
        await session.commit()

        return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


@user_router.post("/signup")
async def signup(request: SignUpRequest):
    """
    Регистрация нового пользователя.

    Args:
        request (SignUpRequest): Данные для регистрации пользователя.
    """

    hashed_password = get_password_hash(request.password)
    async with async_session_maker() as session:
        user = User(
            email=request.email,
            full_name=request.full_name,
            phone_number=request.phone_number,
            password_hash=hashed_password,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return {"message": "Регистрация прошла успешно"}

@user_router.get("/me", response_model=UserSchema)
async def get_me(current_user: UserSchema = Depends(get_current_user)):
    """
    Получение информации о текущем пользователе.

    Args:
        current_user (UserSchema, optional): Текущий аутентифицированный пользователь. Зависимость от `get_current_user`.
    """
    return current_user

@user_router.post("/logout")
async def logout(current_user: UserSchema = Depends(get_current_user)):
    """
    Выход пользователя из системы (удаление токена обновления).

    Args:
        current_user (UserSchema, optional): Текущий аутентифицированный пользователь. Зависимость от `get_current_user`.
    """
    async with async_session_maker() as session:
        user = await session.get(User, current_user.id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.refresh_token = None
        await session.commit()

        return {"message": "Выход прошел успешно"}

