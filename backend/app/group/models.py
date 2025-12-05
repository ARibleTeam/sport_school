from sqlalchemy import Column, Integer, String, Identity, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import select
from app.database import Base, async_session_maker
from typing import List
from app.athlete.models import Athlete

# альтернативный, более простой способ создать отношение между таблицами.
group_athletes = Table(
    "group_athletes",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("athlete_id", ForeignKey("athletes.id"), primary_key=True),
)

group_coaches = Table(
    "group_coaches",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("coach_id", ForeignKey("coaches.id"), primary_key=True),
)

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String, nullable=False)
    
    athletes = relationship("Athlete", secondary=group_athletes, backref="groups")
    coaches = relationship("Coach", secondary=group_coaches, backref="groups")

    def __str__(self):
            return f"Group '{self.name}' (id={self.id})"
    
    @staticmethod
    async def get_all_groups() -> List['Group']:
        """
        Статический метод для получения всех групп.
        """
        async with async_session_maker() as session:
            query = select(Group)
            result = await session.execute(query)
            groups = result.scalars().all()
            return list(groups)

    @staticmethod
    async def get_groups_coach(coach_id: int) -> List['Group']:
        """
        Статический метод для получения групп по ID тренера.
        Запрос исправлен для работы со связью "многие-ко-многим".
        """
        async with async_session_maker() as session:
            # ПРАВИЛЬНЫЙ ЗАПРОС: ищем группы через join с ассоциативной таблицей
            query = select(Group).join(group_coaches).where(group_coaches.c.coach_id == coach_id)
            result = await session.execute(query)
            groups = result.scalars().all()
            return list(groups)

    @staticmethod
    async def get_members(group_id: int) -> List[Athlete]:
        """
        Статический метод для получения участников группы по ID группы.
        """
        async with async_session_maker() as session:
            query = select(Athlete).join(group_athletes).where(group_athletes.c.group_id == group_id)
            result = await session.execute(query)
            athletes = result.scalars().all()
            return list(athletes)

    @staticmethod
    async def get_schedule(athlete_id: int) -> str:
        """
        Статический метод для получения расписания по ID атлета.
        """
        # TODO: Implement logic to get the schedule for the athlete
        print(f"Получение расписания для атлета с ID: {athlete_id}")
        return "{}"
