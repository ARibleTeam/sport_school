from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy import Identity, select
from typing import List, Dict, Optional
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
    groups = relationship("Group", secondary='group_coaches', back_populates="coaches")

    def __str__(self, coach_id: int) -> str:
        return f"Coach ID: {coach_id}"

    @staticmethod
    async def get_coach_id(group_id: int) -> Optional[int]:
        """
        Возвращает ID тренера, связанного с указанной группой.
        Предполагаем, что у группы один основной тренер.
        """
        async with async_session_maker() as session:
            query = (
                select(Coach.id)
                .join(group_coaches)
                .where(group_coaches.c.group_id == group_id)
            )
            result = await session.execute(query)
            # Возвращаем ID первого найденного тренера или None
            return result.scalar_one_or_none()

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
    async def get_upcoming_trainings(coach_id: int) -> List[dict]:
        """
        Собирает расписание тренера и добавляет его имя в каждую тренировку.
        """
        from app.group.models import Group
        from app.training.models import Training

        # 1. Сначала получаем имя тренера, от которого будет идти запрос
        coach_name = await Coach.get_full_name(coach_id)

        all_trainings = []
        # 2. Получаем все группы, которые ведет тренер
        groups = await Group.get_groups_coach(coach_id)

        # 3. Для каждой группы получаем ее "сырое" расписание
        for group in groups:
            group_trainings = await Training.get_upcoming(group.id)
            all_trainings.extend(group_trainings)
        
        # 4. Теперь, когда у нас есть полный список, обогащаем его именем тренера
        for training in all_trainings:
            training["coach"] = coach_name or "Тренер не назначен"
        
        # 5. Сортируем итоговое расписание по дате и времени
        all_trainings.sort(key=lambda x: (x['date'], x['time']))
        
        return all_trainings

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
