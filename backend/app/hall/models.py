from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from sqlalchemy import Identity
from typing import List
from app.training_hall.models import TrainingHall

class Hall(Base):
    __tablename__ = "halls"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String)
    capacity: Mapped[int] = mapped_column(Integer)
    training_halls: Mapped[List[TrainingHall]] = relationship("TrainingHall", back_populates="hall")

    def __str__(self, hall_id: int) -> str:
        return f"Hall ID: {hall_id}"

    @staticmethod
    def get_hall(training_id: int) -> str:
        pass

    @staticmethod
    def is_available(hall_id: int, start_time, end_time) -> bool:
        pass