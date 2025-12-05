from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.coach.schemas import CoachSchema, CoachResponseSchema
from app.coach.models import Coach
from sqlalchemy import select
from app.middleware import get_current_user
from app.user.schemas import UserSchema
from app.specialization.models import SportType
from app.database import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession

coach_router = APIRouter(prefix="/coaches", tags=["ТРЕНЕР"])

@coach_router.get("/", response_model=List[CoachSchema], summary="Получение списка тренеров")
async def get_coaches(current_user: UserSchema = Depends(get_current_user)) -> List[CoachSchema]:
    return await Coach.get_coaches()

@coach_router.get("/{id}", response_model=CoachResponseSchema, summary="Получение данных тренера по ID")
async def get_coach(id: int, current_user: UserSchema = Depends(get_current_user)):
    async with async_session_maker() as session:
        coach = await session.get(Coach, id)
        if not coach:
            raise HTTPException(status_code=404, detail="Тренер не найден")

        contact_info = Coach.get_contact_info(coach.id)
        specializations = await SportType.get_specializations(coach.id)

        coach_data = CoachSchema(
            id=coach.id,
            experience_years=coach.experience_years,
            bio=coach.bio,
            full_name=coach.full_name,
            email=contact_info.get("email"),
            specialization=specializations
        )

        # TODO: Implement logic to get the schedule for the coach
        schedule = await Coach.get_upcoming_trainings(coach.id)

        return CoachResponseSchema(trainer=coach_data, schedule=schedule)
