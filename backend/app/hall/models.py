from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import Base, async_session_maker
from sqlalchemy import select
from app.training_hall.models import TrainingHall

class Hall(Base):
    __tablename__ = "halls"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)

    training_halls = relationship("TrainingHall", back_populates="hall")

    def __repr__(self):
        return f"<Hall(id={self.id}, name='{self.name}', capacity={self.capacity})>"

    @staticmethod
    async def get_hall(training_id: int) -> str:
        """
        Возвращает название зала, связанного с указанной тренировкой.

        Args:
            training_id: ID тренировки.

        Returns:
            Название зала или "Неизвестно", если зал не найден.
        """
        async with async_session_maker() as session:
            query = select(Hall.name).join(
                TrainingHall
            ).where(
                TrainingHall.training_id == training_id
            )
            result = await session.execute(query)
            hall_name = result.scalar_one_or_none()
            return hall_name if hall_name else "Неизвестно"

    @staticmethod
    def is_available(hall_id: int, start_time, end_time) -> bool:
        pass