from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, async_session_maker
from sqlalchemy import Identity, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)

    def __str__(self):
        return f"User(id={self.id})"

    @staticmethod
    async def is_admin(user_id: int) -> bool:
        async with async_session_maker() as session:
            user = await session.get(User, user_id)
            if user:
                # Здесь должна быть логика проверки, является ли пользователь админом
                # Например, проверка наличия роли "admin" у пользователя
                return True  # Заглушка
            return False

    @staticmethod
    async def is_coach(user_id: int) -> bool:
        async with async_session_maker() as session:
            user = await session.get(User, user_id)
            if user:
                # Здесь должна быть логика проверки, является ли пользователь тренером
                return False  # Заглушка
            return False

    @staticmethod
    async def is_athlete(user_id: int) -> bool:
        async with async_session_maker() as session:
            user = await session.get(User, user_id)
            if user:
                # Здесь должна быть логика проверки, является ли пользователь атлетом
                return True  # Заглушка
        return False

