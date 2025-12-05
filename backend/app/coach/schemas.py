from pydantic import BaseModel
from typing import List, Optional

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
    type: str  # 'individual' or 'group'
    title: str
    time: str
    location: str
    date: str
    coach: str
    participants: Optional[int] = None

class CoachResponseSchema(BaseModel):
    trainer: CoachSchema
    schedule: List[TrainingSchema]