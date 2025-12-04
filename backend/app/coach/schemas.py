from pydantic import BaseModel
from typing import List

class CoachSchema(BaseModel):
    id: int
    experience_years: int
    bio: str
    full_name: str
    email: str
    specialization: list[str]

    class Config:
        from_attributes = True

class TrainingSchema(BaseModel):
    id: int
    type: str
    title: str
    time: str
    location: str
    date: str
    participants: int | None = None

class CoachResponseSchema(BaseModel):
    trainer: CoachSchema
    schedule: List[TrainingSchema]
