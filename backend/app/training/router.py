from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import async_session_maker
from app.training.schemas import TrainingSchema, TrainingType
from app.training.models import Training
from app.middleware import get_current_user
from app.user.schemas import UserSchema
from datetime import datetime, date
from app.hall.models import Hall

training_router = APIRouter(prefix="/schedule", tags=["Расписание"])

@training_router.get("/", response_model=List[TrainingSchema])
async def get_schedule(
    type: Optional[TrainingType] = Query(None, description="Тип тренировки"),
    current_user: UserSchema = Depends(get_current_user),
):
    async with async_session_maker() as session:
        query = select(Training)
        if type:
            query = query.where(Training.is_group_training == (type == TrainingType.group))

        result = await session.execute(query)
        trainings = result.scalars().all()

        training_schemas = []
        for training in trainings:
            # Get hall name
            hall_name = await Hall.get_hall(training.id)

            training_schema = TrainingSchema(
                id=training.id,
                coach="Неизвестный тренер",
                type=TrainingType.group if training.is_group_training else TrainingType.individual,
                title="Тренировка",
                time=training.start_time.strftime("%H:%M"),
                location=hall_name,
                date=training.start_time.date(),
                participants=0,
            )
            training_schemas.append(training_schema)

        return training_schemas
