from pydantic import BaseModel
from enum import Enum
from datetime import date, datetime

class TrainingType(str, Enum):
    individual = "individual"
    group = "group"

class TrainingSchema(BaseModel):
    id: int
    coach: str
    type: TrainingType
    title: str
    time: str
    location: str
    date: date
    participants: int

    class Config:
        from_attributes = True

class CreateTrainingRequest(BaseModel):
    start_time: datetime
    end_time: datetime
    group_id: int
    hall_id: int