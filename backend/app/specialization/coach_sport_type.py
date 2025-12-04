from sqlalchemy import Column, Integer, ForeignKey, Table  #  Table не нужно, это модель
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class CoachSportType(Base):
    __tablename__ = "coach_sport_types"
    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id"), primary_key=True)
    sport_type_id: Mapped[int] = mapped_column(ForeignKey("sport_types.id"), primary_key=True)
    
    coach = relationship("Coach", back_populates="coach_sport_types")
    sport_type = relationship("SportType", back_populates="coaches")