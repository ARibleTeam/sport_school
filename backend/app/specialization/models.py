from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy import Identity
from typing import List
from app.group.models import group_coaches
from app.database import async_session_maker
from app.specialization.coach_sport_type import CoachSportType # Импортируем CoachSportType

class SportType(Base):
    __tablename__ = "sport_types"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    coaches = relationship("CoachSportType", back_populates="sport_type")

    def __str__(self, sport_type_id: int) -> str:
        return f"SportType ID: {sport_type_id}"

    @staticmethod
    async def get_specializations(coach_id: int) -> List[str]:
        async with async_session_maker() as session:
            specializations = await session.execute(
                select(SportType.name)
                .join(CoachSportType, CoachSportType.sport_type_id == SportType.id)
                .where(CoachSportType.coach_id == coach_id)
            )
            return [specialization[0] for specialization in specializations.all()]  # Return a list of sport type names

    @staticmethod
    async def get_sport_type_group(group_id: int) -> List[str]:
        """
        Статический метод для получения названий специализаций,
        связанных с тренерами указанной группы.
        """
        async with async_session_maker() as session:
            # Запрос, который связывает SportType -> CoachSportType -> group_coaches
            query = (
                select(SportType.name)
                .join(CoachSportType, CoachSportType.sport_type_id == SportType.id)
                .join(group_coaches, group_coaches.c.coach_id == CoachSportType.coach_id)
                .where(group_coaches.c.group_id == group_id)
                .distinct()
            )
            result = await session.execute(query)
            return result.scalars().all()