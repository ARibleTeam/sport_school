import random
from datetime import datetime, timedelta, timezone 
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

        # 4. Создание уникальных тренеров
        print("Создание уникальных тренеров...")

        # Список с данными для каждого тренера
        coaches_data = [
            {
                "full_name": "Иван Петрович Сергеев",
                "email": "ivan.sergeev@school.com",
                "experience": 25,
                "bio": "Заслуженный тренер по плаванию. Воспитал не одно поколение чемпионов. Подход строгий, но справедливый. Главное — дисциплина и полная самоотдача.",
                "specializations": ["Плавание"]
            },
            {
                "full_name": "Артем Сидоров",
                "email": "artem.sidorov@school.com",
                "experience": 10,
                "bio": "Бывший профессиональный боксер, призер международных соревнований. Ставлю ударную технику и учу думать на ринге. Мои ученики — моя гордость.",
                "specializations": ["Бокс"]
            },
            {
                "full_name": "Елена Воробьева",
                "email": "elena.vorobyova@school.com",
                "experience": 8,
                "bio": "Сертифицированный CrossFit Level 3 тренер. Верю, что нет предела человеческим возможностям. Создаю дружелюбную атмосферу, где каждый сможет превзойти себя.",
                "specializations": ["Кроссфит", "Функциональный тренинг"]
            },
            {
                "full_name": "Анастасия Лазарева",
                "email": "anastasia.lazareva@school.com",
                "experience": 12,
                "bio": "Практикую йогу более 15 лет. Помогу вам найти гармонию между телом и разумом, развить гибкость и снять стресс. Мои занятия — это путешествие внутрь себя.",
                "specializations": ["Йога", "Пилатес"]
            },
            {
                "full_name": "Антон Медоедов",
                "email": "anton.medoedov.@school.com",
                "experience": 20,
                "bio": "Мастер спорта по тяжелой атлетике. Знаю все о работе с железом. Помогу набрать массу, увеличить силовые показатели и построить тело мечты. Без лишних слов, только хардкор.",
                "specializations": ["Тяжелая атлетика"]
            }
        ]

        # Создаем экземпляры класса Coach и добавляем в сессию
        coaches = []
        for data in coaches_data:
            # Убедимся, что это имя еще не использовалось
            if data["full_name"] not in used_names:
                coach = Coach(
                    full_name=data["full_name"],
                    email=data["email"],
                    password_hash=get_password_hash("password"),
                    phone_number=f"+7999{random.randint(1000000, 9999999)}",
                    experience_years=data["experience"],
                    bio=data["bio"]
                )
                coaches.append(coach)
                used_names.add(data["full_name"])

        session.add_all(coaches)
        await session.flush()  # Получаем ID для созданных тренеров

        # Создаем связи между тренерами и их специализациями
        coach_links = []
        # Создадим словарь для быстрого поиска тренера по имени
        coaches_map = {coach.full_name: coach for coach in coaches}

        for data in coaches_data:
            coach = coaches_map.get(data["full_name"])
            if coach:
                for spec_name in data["specializations"]:
                    sport_type = sport_types_map.get(spec_name)
                    if sport_type:
                        coach_links.append(
                            CoachSportType(coach_id=coach.id, sport_type_id=sport_type.id)
                        )

        session.add_all(coach_links)
        print("7 уникальных тренеров и их специализации созданы.")
        
        # 5. Создание Атлетов (30)
        print("Создание атлетов...")
        athletes = []

        # 5.1. Создаем одного известного атлета для входа
        known_athlete_name = "Антонов Игорь Алексеевич"
        known_athlete = Athlete(
            full_name=known_athlete_name,
            email="test@test.com",
            password_hash=get_password_hash("string"), # Легко запоминаемый пароль
            phone_number="+79990001122"
        )
        athletes.append(known_athlete)
        used_names.add(known_athlete_name) # Добавляем имя в список использованных
        print("Добавлен тестовый атлет для входа: email='test@test.com', password='string'")

        # 5.2. Создаем остальных 29 случайных атлетов
        for _ in range(29):
            athletes.append(Athlete(
                full_name=generate_full_name(used_names),
                email=f"athlete.{len(used_names)}@school.com",
                password_hash=get_password_hash("password"),
                phone_number=f"+7900{random.randint(1000000, 9999999)}",
            ))
        session.add_all(athletes)
        print("Остальные 29 атлетов созданы.")
        
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
                
                # ИЗМЕНЕНИЕ ЗДЕСЬ: Используем timezone.utc для создания "aware" datetime
                start = datetime.now(timezone.utc).replace(hour=hour, minute=0, second=0, microsecond=0) + timedelta(days=day)
                
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