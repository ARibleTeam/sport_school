from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class TrainingHall(Base):
    __tablename__ = "training_halls"

    training_id: Mapped[int] = mapped_column(ForeignKey("trainings.id"), primary_key=True)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id"), primary_key=True)

    training: Mapped["Training"] = relationship("Training", back_populates="training_halls")
    hall: Mapped["Hall"] = relationship("Hall", back_populates="training_halls")
