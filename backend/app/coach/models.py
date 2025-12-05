from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy import Identity, select
from typing import List, Dict
from app.specialization.models import SportType
from app.specialization.coach_sport_type import CoachSportType # Импортируем CoachSportType
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.coach.schemas import CoachSchema
from app.user.models import User
from app.group.models import group_coaches

class Coach(User):
    __tablename__ = "coaches"

    id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    experience_years: Mapped[int] = mapped_column(Integer)
    bio: Mapped[str] = mapped_column(String)
    
    coach_sport_types = relationship("CoachSportType", back_populates="coach")
    groups = relationship("Group", secondary=group_coaches, back_populates="coaches")

    def __str__(self, coach_id: int) -> str:
        return f"Coach ID: {coach_id}"

    @staticmethod
    def get_coach_id(group_id: int) -> int:
            pass

    @staticmethod
    async def get_coaches() -> List[CoachSchema]:
        async with async_session_maker() as session:
            result = await session.execute(select(Coach))
            coaches = result.scalars().all()
            coach_schemas = []
            for coach in coaches:
                coach_id = coach.id
                contact_info = Coach.get_contact_info(coach_id)
                specializations = await SportType.get_specializations(coach_id)
                coach_schema = CoachSchema(
                    id=coach_id,
                    experience_years=await Coach.get_experience_years(coach_id),
                    bio=await Coach.get_bio(coach_id),
                    full_name=await Coach.get_full_name(coach_id),
                    email=contact_info.get("email"),
                    specialization=specializations
                )
                coach_schemas.append(coach_schema)
            return coach_schemas

    @staticmethod
    async def get_full_name(coach_id: int) -> str:
        async with async_session_maker() as session:
            coach = await session.execute(select(User.full_name).join(Coach).where(Coach.id == coach_id))
            coach = coach.scalar_one_or_none()
            return coach

    @staticmethod
    async def get_experience_years(coach_id: int) -> int:
        async with async_session_maker() as session:
            coach = await session.execute(select(Coach.experience_years).where(Coach.id == coach_id))
            coach = coach.scalar_one_or_none()
            return coach

    @staticmethod
    async def get_bio(coach_id: int) -> str:
        async with async_session_maker() as session:
            coach = await session.execute(select(Coach.bio).where(Coach.id == coach_id))
            coach = coach.scalar_one_or_none()
            return coach

    @staticmethod
    def get_upcoming_trainings(coach_id: int) -> JSON:
            pass

    @staticmethod
    def get_contact_info(coach_id: int) -> Dict[str, str]:
            # TODO: Implement logic to get contact info by coach ID
        return {"phone": "+79991234567", "email": "coach@example.com"}  # Placeholder

    @staticmethod
    def create_coach(user_id: int) -> bool:
            pass

    @staticmethod
    def is_available(coach_id: int, start_time, end_time) -> bool:
            pass
