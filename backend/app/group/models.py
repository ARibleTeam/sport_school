from sqlalchemy import Column, Integer, String, Identity, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import select
from app.database import Base, async_session_maker
from typing import List
from app.athlete.models import Athlete

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

training_groups = Table(
    "training_groups",
    Base.metadata,
    Column("training_id", ForeignKey("trainings.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String, nullable=False)
    
    athletes = relationship("Athlete", secondary=group_athletes, back_populates="groups")
    coaches = relationship("Coach", secondary=group_coaches, back_populates="groups")
    trainings = relationship("Training", secondary=training_groups, back_populates="groups")

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
    async def get_schedule(athlete_id: int) -> List[dict]:
        """
        Главный метод-оркестратор для получения расписания атлета.
        Реализован в соответствии с диаграммой последовательности.
        """
        from app.training.models import Training
        from app.coach.models import Coach

        all_trainings = []

        # 1. Находим все группы, в которых состоит атлет
        async with async_session_maker() as session:
            groups_query = select(Group).join(group_athletes).where(group_athletes.c.athlete_id == athlete_id)
            groups_result = await session.execute(groups_query)
            groups = groups_result.scalars().all()

        # 2. Для каждой группы собираем полное расписание
        for group in groups:
            # 2.1 Получаем "сырое" расписание (без имени тренера)
            group_trainings = await Training.get_upcoming(group.id)

            # 2.2 Получаем ID тренера и его имя
            coach_id = await Coach.get_coach_id(group.id)
            coach_name = "Тренер не назначен"
            if coach_id:
                coach_name = await Coach.get_full_name(coach_id)
            
            # 2.3 Обогащаем каждую тренировку именем тренера
            for training in group_trainings:
                training["coach"] = coach_name
            
            all_trainings.extend(group_trainings)
        
        # 3. Сортируем итоговое расписание и возвращаем
        all_trainings.sort(key=lambda x: (x['date'], x['time']))
        return all_trainings