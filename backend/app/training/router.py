from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import async_session_maker
from app.training.schemas import TrainingSchema, TrainingType, CreateTrainingRequest
from app.training.models import Training
from app.middleware import get_current_user
from app.user.schemas import UserSchema
from datetime import datetime, date
from app.hall.models import Hall
from app.group.models import Group

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

@training_router.post(
    "/", 
    summary="Создание новой тренировки",
    status_code=status.HTTP_201_CREATED,
    response_description="Тренировка успешно создана"
)
async def create_training(
    training_data: CreateTrainingRequest,
    # TODO: Добавить проверку, что пользователь является администратором или тренером
    current_user: UserSchema = Depends(get_current_user) 
):
    """
    Создает новую тренировку с проверкой доступности зала и тренера.
    
    - **start_time**: Время начала в формате ISO (например, "2025-12-10T10:00:00")
    - **end_time**: Время окончания в формате ISO (например, "2025-12-10T11:30:00")
    - **group_id**: ID группы, для которой создается тренировка
    - **hall_id**: ID зала, в котором будет проходить тренировка
    """
    # Вызываем наш статический метод с логикой
    success, message = await Training.create_training(
        start_time=training_data.start_time,
        end_time=training_data.end_time,
        group_id=training_data.group_id,
        hall_id=training_data.hall_id,
    )

    # Если метод вернул ошибку, выбрасываем исключение
    if not success:
        raise HTTPException(
            # 409 Conflict - подходящий код для конфликта расписаний
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )
    
    # В случае успеха возвращаем сообщение
    return {"message": message}