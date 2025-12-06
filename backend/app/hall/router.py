from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from app.database import async_session_maker
from app.hall.schemas import HallSchema
from app.hall.models import Hall
from app.middleware import get_current_user
from app.user.schemas import UserSchema

hall_router = APIRouter(prefix="/halls", tags=["Залы"])

@hall_router.get("/", response_model=List[HallSchema], summary="Получение списка всех залов")
async def get_halls(current_user: UserSchema = Depends(get_current_user)):
    """
    Возвращает список всех доступных залов.
    """
    async with async_session_maker() as session:
        result = await session.execute(select(Hall))
        halls = result.scalars().all()
        return halls