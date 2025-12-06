from sqlalchemy import Column, Integer, DateTime, Boolean, JSON, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from app.database import Base, async_session_maker
from sqlalchemy import Identity
from typing import List
from typing import Tuple
from datetime import datetime as dt
from app.training_hall.models import TrainingHall

class Training(Base):
    __tablename__ = "trainings"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    start_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    is_group_training: Mapped[Boolean] = mapped_column(Boolean)

    training_halls: Mapped[List[TrainingHall]] = relationship("TrainingHall", back_populates="training")
    groups: Mapped[List["Group"]] = relationship( # type: ignore
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
    async def create_training(
        start_time: dt, 
        end_time: dt, 
        group_id: int, 
        hall_id: int
    ) -> Tuple[bool, str]: # <- ИЗМЕНЯЕМ ВОЗВРАЩАЕМЫЙ ТИП
        """
        Создает новую тренировку с проверкой доступности зала и тренера.
        Возвращает кортеж (успех: bool, сообщение: str).
        """
        # Локальные импорты
        from app.group.models import Group
        from app.hall.models import Hall
        from app.coach.models import Coach
        from app.training_hall.models import TrainingHall
        
        async with async_session_maker() as session:
            try:
                # --- ЭТАП ПРОВЕРОК ---

                # 1. Проверяем доступность зала
                if not await Hall.is_available(hall_id, start_time, end_time):
                    return (False, f"Зал с ID={hall_id} уже занят в это время.")

                # 2. Получаем тренера группы для проверки его доступности
                coach_id = await Coach.get_coach_id(group_id)
                if coach_id:
                    if not await Coach.is_available(coach_id, start_time, end_time):
                        return (False, f"Тренер с ID={coach_id} уже занят в это время.")
                
                # --- ЭТАП СОЗДАНИЯ ---

                group_query = select(Group).where(Group.id == group_id).options(selectinload(Group.athletes))
                group = (await session.execute(group_query)).scalar_one_or_none()
                hall = await session.get(Hall, hall_id)

                if not group or not hall:
                    return (False, f"Группа с id={group_id} или Зал с id={hall_id} не найдены.")
                
                is_group = len(group.athletes) > 1
                
                new_training = Training(
                    start_time=start_time, end_time=end_time, is_group_training=is_group
                )
                
                new_training.groups.append(group)
                session.add(new_training)
                await session.flush()
                
                session.add(TrainingHall(training_id=new_training.id, hall_id=hall.id))
                
                await session.commit()
                
                message = f"Успешно создана {'групповая' if is_group else 'индивидуальная'} тренировка с ID={new_training.id}"
                return (True, message)

            except Exception as e:
                await session.rollback()
                print(f"Ошибка при создании тренировки: {e}")
                return (False, f"Внутренняя ошибка сервера: {e}")
