from typing import List
from fastapi import APIRouter, Depends
from app.group.schemas import GroupSchema
from app.group.models import Group
from app.middleware import get_current_user
from app.user.schemas import UserSchema

group_router = APIRouter(prefix="/groups", tags=["Группы"])

@group_router.get("/", response_model=List[GroupSchema], summary="Получение списка всех групп")
async def get_groups(current_user: UserSchema = Depends(get_current_user)):
    """
    Возвращает список всех тренировочных групп.
    """
    return await Group.get_all_groups()