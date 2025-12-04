from sqlalchemy import Column, Integer, DateTime, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy import Identity
from typing import List
from app.training_hall.models import TrainingHall

class Training(Base):
    __tablename__ = "trainings"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    start_time: Mapped[DateTime] = mapped_column(DateTime)
    end_time: Mapped[DateTime] = mapped_column(DateTime)
    is_group_training: Mapped[Boolean] = mapped_column(Boolean)
    training_halls: Mapped[List[TrainingHall]] = relationship("TrainingHall", back_populates="training")

    def __str__(self, training_id: int) -> str:
        return f"Training ID: {training_id}"

    @staticmethod
    def get_duration(training_id: int) -> float:
        pass

    @staticmethod
    def get_upcoming(group_id: int) -> JSON:
        pass

    @staticmethod
    def get_all_trainings() -> List['Training']:
        pass

    @staticmethod
    def is_upcoming(training_id: int) -> bool:
        pass

    @staticmethod
    def is_ongoing(training_id: int) -> bool:
        pass

    @staticmethod
    def is_completed(training_id: int) -> bool:
        pass

    @staticmethod
    def create_training(start_time, end_time, group_id, hall_id) -> bool:
        pass
