from sqlalchemy import Column, Integer, String, Identity, select, exists
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.database import Base, async_session_maker
from app.training_hall.models import TrainingHall
# ДОБАВЬТЕ ЭТИ ИМПОРТЫ
from datetime import datetime as dt


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
    async def is_available(hall_id: int, start_time: dt, end_time: dt) -> bool:
        """
        Проверяет, свободен ли зал в указанный временной интервал.
        Возвращает True, если свободен, и False, если есть пересечение.
        """
        # Локальные импорты, чтобы избежать циклических зависимостей
        from app.training.models import Training
        from app.training_hall.models import TrainingHall
        
        async with async_session_maker() as session:
            # Логика проверки пересечения интервалов:
            # (StartA < EndB) and (EndA > StartB)
            # Нам нужно найти хотя бы ОДНУ тренировку, которая пересекается.
            # EXISTS() в SQL - самый эффективный способ для этого.
            overlap_query = select(Training.id).join(TrainingHall).where(
                TrainingHall.hall_id == hall_id,
                Training.start_time < end_time,
                Training.end_time > start_time
            )
            
            # Мы проверяем, существует ли хотя бы одна такая запись
            overlapping_training_exists = await session.execute(
                select(exists(overlap_query))
            )
            
            # Если пересекающаяся тренировка существует, scalar() вернет True.
            # Нам нужно вернуть обратное значение: зал НЕ доступен, если что-то найдено.
            return not overlapping_training_exists.scalar()