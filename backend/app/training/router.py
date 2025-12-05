from app.group.models import Group
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
    type: Optional[TrainingType] = Query(None, description="Тип тренировки: 'individual' или 'group'"),
    current_user: UserSchema = Depends(get_current_user),
):
    # 1. Получаем полный список расписания, как и раньше
    full_schedule = await Group.get_schedule(athlete_id=current_user.id)

    # 2. Если query-параметр 'type' был передан, фильтруем результат уже в роутере
    if type:
        # type.value вернет строку 'individual' или 'group'
        # Мы создаем новый список, включая только те словари, где поле 'type' совпадает
        filtered_schedule = [
            training for training in full_schedule if training.get("type") == type.value
        ]
        return filtered_schedule

    # 3. Если фильтр не был указан, возвращаем полный список
    return full_schedule
