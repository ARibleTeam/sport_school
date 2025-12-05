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

    athletes = relationship("Athlete", secondary=group_athletes, backref="groups")
    coaches = relationship("Coach", secondary=group_coaches, backref="groups")

    def __str__(self):
        return f"Group(id={self.id})"

    async def get_all_groups(self) -> List['Group']:
        async with async_session_maker() as session:
            query = select(Group)
            result = await session.execute(query)
            groups = result.scalars().all()
            return list(groups)

    async def get_groups_coach(self, coach_id: int) -> List['Group']:
        async with async_session_maker() as session:
            query = select(Group).where(Group.coach_id == coach_id)
            result = await session.execute(query)
            groups = result.scalars().all()
            return list(groups)

    async def get_members(self, group_id: int) -> List[Athlete]:
         async with async_session_maker() as session:
            query = select(Athlete).join(group_athletes).where(group_athletes.c.group_id == group_id)
            result = await session.execute(query)
            athletes = result.scalars().all()
            return list(athletes)

    async def get_schedule(self, athlete_id: int) -> str:
        # TODO: Implement logic to get the schedule for the athlete
        return "{}"
