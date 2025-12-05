from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import select

from app.database import Base, async_session_maker
from typing import List
from app.user.models import User


class Athlete(User):
    __tablename__ = "athletes"

    id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)

    def __str__(self) -> str:
        return f"Athlete(id={self.id}, full_name={self.full_name})"

    @staticmethod
    async def get_full_name(user_id: int) -> str:
        async with async_session_maker() as session:
            user = await session.execute(select(User.full_name).where(User.id == user_id))
            full_name = user.scalar_one_or_none()
            return full_name

    @staticmethod
    async def get_weekly_load(user_id: int) -> float:
        pass

    @staticmethod
    async def create_athlete(user_id: int) -> bool:
        pass
