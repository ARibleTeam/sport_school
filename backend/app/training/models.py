from sqlalchemy import Column, Integer, DateTime, Boolean, JSON, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, async_session_maker
from sqlalchemy import Identity
from typing import List
from app.training_hall.models import TrainingHall

class Training(Base):
    __tablename__ = "trainings"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    start_time: Mapped[DateTime] = mapped_column(DateTime)
    end_time: Mapped[DateTime] = mapped_column(DateTime)
    is_group_training: Mapped[Boolean] = mapped_column(Boolean)
    training_halls: Mapped[List[TrainingHall]] = relationship("TrainingHall", back_populates="training")
    
    groups: Mapped[List["Group"]] = relationship(
        "Group", 
        secondary="training_groups", 
        back_populates="trainings"
    )
    
    def __str__(self, training_id: int) -> str:
        return f"Training ID: {training_id}"

    @staticmethod
    def get_duration(training_id: int) -> float:
        pass

    @staticmethod
    async def get_upcoming(group_id: int) -> List[dict]:
        """
        Получает все предстоящие тренировки для указанной группы.
        НЕ ДОБАВЛЯЕТ ИМЯ ТРЕНЕРА.
        """
        # Локальные импорты для избежания циклических зависимостей
        from app.group.models import Group, training_groups
        from app.hall.models import Hall
        from app.specialization.models import SportType

        async with async_session_maker() as session:
            # 1. Получаем все объекты тренировок для данной группы
            trainings_query = select(Training).join(training_groups).where(training_groups.c.group_id == group_id)
            trainings_result = await session.execute(trainings_query)
            trainings = trainings_result.scalars().all()

            if not trainings:
                return []

            # 2. Получаем общую информацию о группе ОДИН РАЗ
            group_members = await Group.get_members(group_id)
            group_specializations = await SportType.get_sport_type_group(group_id)
            
            # 3. Формируем список тренировок, обогащая каждую данными
            schedule_list = []
            for training in trainings:
                hall_name = await Hall.get_hall(training.id)
                title = f"Тренировка по {group_specializations[0]}" if group_specializations else "Групповая тренировка"

                schedule_list.append({
                    "id": training.id,
                    # КЛЮЧ "coach" УДАЛЕН. Он будет добавлен на более высоком уровне.
                    "type": 'group' if training.is_group_training else 'individual',
                    "title": title,
                    "time": training.start_time.strftime("%H:%M"),
                    "location": hall_name or "Зал не указан",
                    "date": training.start_time.strftime("%Y-%m-%d"),
                    "participants": len(group_members)
                })
        
            return schedule_list

    @staticmethod
    def get_all_trainings() -> List['Training']:
        pass

    @staticmethod
    def is_upcoming(training_id: int) -> bool:
        pass

    @staticmethod
    def is_ongoing(training_id: int) -> bool:
        pass

    @staticmethod
    def is_completed(training_id: int) -> bool:
        pass

    @staticmethod
    def create_training(start_time, end_time, group_id, hall_id) -> bool:
        pass
