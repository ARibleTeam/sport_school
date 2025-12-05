import random
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload

from app.database import async_session_maker, Base
from app.config import settings
from app.utils import get_password_hash

# Импортируем все необходимые модели
from app.coach.models import Coach
from app.athlete.models import Athlete
from app.user.models import User
from app.group.models import Group
from app.training.models import Training
from app.hall.models import Hall
from app.specialization.models import SportType, CoachSportType
from app.training_hall.models import TrainingHall


test_router = APIRouter(prefix="/tests", tags=["ТЕСТОВЫЕ ДАННЫЕ"])

# --- Данные для генерации ---

MALE_NAMES = ["Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Артем", "Илья", "Кирилл", "Михаил"]
FEMALE_NAMES = ["Анастасия", "Мария", "Анна", "Дарья", "Екатерина", "Полина", "Виктория", "Елизавета", "Александра", "София"]
SURNAMES = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров", "Соколов", "Михайлов", "Новиков", "Федоров"]

def generate_full_name(used_names_set):
    """Генерирует уникальное ФИО и добавляет его в set."""
    while True:
        is_male = random.choice([True, False])
        surname = random.choice(SURNAMES)
        if not is_male:
            surname += "а"
        
        name = f"{surname} {random.choice(MALE_NAMES if is_male else FEMALE_NAMES)}"
        
        if name not in used_names_set:
            used_names_set.add(name)
            return name

# --- Эндпоинты ---

@test_router.post("/seed", summary="Создать полный набор тестовых данных")
async def seed_database():
    """
    Создает полный набор логически связанных данных: типы спорта, залы, 7 тренеров,
    30 атлетов, 4 группы и по 5 тренировок для каждой группы.
    Если данные уже существуют, операция будет отменена.
    """
    async with async_session_maker() as session:
        # 1. Проверка: Если данные уже есть, отменяем операцию
        check_coaches = await session.execute(select(Coach))
        if check_coaches.scalars().first():
            raise HTTPException(status_code=409, detail="Данные уже существуют. Сначала очистите базу данных через /tests/clear.")

        print("--- Начало создания тестовых данных ---")
        
        # 2. Создание базовых данных: Типы спорта
        print("Создание типов спорта...")
        sport_types_data = [
            {"name": "Плавание", "description": "Отработка техники плавания."},
            {"name": "Бокс", "description": "Освоение ударной техники."},
            {"name": "Йога", "description": "Практика асан и медитации."},
            {"name": "Кроссфит", "description": "Высокоинтенсивные функциональные тренировки."},
            {"name": "Тяжелая атлетика", "description": "Работа со штангой."},
            {"name": "Борьба", "description": "Изучение техник единоборств."},
        ]
        sport_types = [SportType(**data) for data in sport_types_data]
        session.add_all(sport_types)
        await session.flush()
        sport_types_map = {st.name: st for st in sport_types}
        print("Типы спорта созданы.")

        # 3. Создание базовых данных: Залы
        print("Создание залов...")
        halls_data = [
            {"name": "Бассейн 1", "capacity": 30},
            {"name": "Зал бокса", "capacity": 20},
            {"name": "Кроссфит зона", "capacity": 40},
            {"name": "Зал для йоги (№2)", "capacity": 50},
        ]
        halls = [Hall(**data) for data in halls_data]
        session.add_all(halls)
        await session.flush()
        halls_map = {h.name: h for h in halls}
        print("Залы созданы.")

        used_names = set()

        # 4. Создание Тренеров (7)
        print("Создание тренеров...")
        coaches = []
        for _ in range(7):
            coaches.append(Coach(
                full_name=generate_full_name(used_names),
                email=f"coach.{len(used_names)}@school.com",
                password_hash=get_password_hash("password"),
                phone_number=f"+7999{random.randint(1000000, 9999999)}",
                experience_years=random.randint(2, 15),
                bio="Опытный специалист, нацеленный на результат."
            ))
        session.add_all(coaches)
        await session.flush()

        # 4.1. Назначение специализаций тренерам
        required_specs = ["Плавание", "Бокс", "Кроссфит", "Йога"]
        for i, spec_name in enumerate(required_specs):
            session.add(CoachSportType(coach_id=coaches[i].id, sport_type_id=sport_types_map[spec_name].id))
        
        for coach in coaches[len(required_specs):]:
            spec = random.choice(sport_types)
            session.add(CoachSportType(coach_id=coach.id, sport_type_id=spec.id))
        print("Тренеры и их специализации созданы.")
        
        # 5. Создание Атлетов (30)
        print("Создание атлетов...")
        athletes = []
        for _ in range(30):
            athletes.append(Athlete(
                full_name=generate_full_name(used_names),
                email=f"athlete.{len(used_names)}@school.com",
                password_hash=get_password_hash("password"),
                phone_number=f"+7900{random.randint(1000000, 9999999)}",
            ))
        session.add_all(athletes)
        print("Атлеты созданы.")
        
        await session.commit() # Сохраняем все созданные сущности

        # 6. Создание Групп (4) и их наполнение
        print("Создание групп и распределение участников...")
        group_defs = [
            {"name": "Пловцы-Юниоры", "sport": "Плавание", "hall_pref": "Бассейн 1", "coach_idx": 0},
            {"name": "Боксеры-Новички", "sport": "Бокс", "hall_pref": "Зал бокса", "coach_idx": 1},
            {"name": "Энергия-Кроссфит", "sport": "Кроссфит", "hall_pref": "Кроссфит зона", "coach_idx": 2},
            {"name": "Утренняя Йога", "sport": "Йога", "hall_pref": "Зал для йоги (№2)", "coach_idx": 3},
        ]
        
        for i, group_def in enumerate(group_defs):
            group = Group(name=group_def["name"])
            group.coaches.append(coaches[group_def["coach_idx"]])
            
            # Распределяем атлетов по группам
            start_idx = i * 7
            group.athletes.extend(athletes[start_idx : start_idx + 7])
            session.add(group)
            
            # 7. Создание Тренировок для каждой группы (по 5)
            await session.flush() # Получаем ID группы
            
            hall = halls_map[group_def["hall_pref"]]
            for j in range(5):
                day = random.randint(1, 7)
                hour = random.choice([9, 11, 14, 16, 18])
                start = datetime.now().replace(hour=hour, minute=0, second=0) + timedelta(days=day)
                
                training = Training(
                    start_time=start,
                    end_time=start + timedelta(hours=1, minutes=30),
                    is_group_training=(j < 4) # 4 групповых, 1 индивидуальная
                )
                training.groups.append(group)
                session.add(training)
                await session.flush() # Получаем ID тренировки
                session.add(TrainingHall(training_id=training.id, hall_id=hall.id))
        
        print("Группы и тренировки созданы.")
        
        await session.commit()
        print("--- Все тестовые данные успешно созданы! ---")

    return {"message": "Полный набор тестовых данных успешно создан!"}


@test_router.post("/clear", summary="ПОЛНАЯ ОЧИСТКА ВСЕХ ДАННЫХ")
async def clear_database():
    """
    Удаляет все данные из всех таблиц и сбрасывает счетчики ID.
    КРАЙНЕ ОПАСНО! Работает только если в .env файле DEBUG=True.
    """
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Очистка базы данных разрешена только в режиме отладки.")

    async with async_session_maker() as session:
        table_names = [table.name for table in reversed(Base.metadata.sorted_tables)]
        if not table_names:
            return {"message": "Не найдено таблиц для очистки."}

        # Выполняем единый SQL-запрос для быстрой очистки
        query = text(f'TRUNCATE TABLE {", ".join(table_names)} RESTART IDENTITY CASCADE;')
        
        await session.execute(query)
        await session.commit()
        
        print(f"База данных успешно очищена. Таблицы: {table_names}")

    return {"message": "База данных успешно очищена."}