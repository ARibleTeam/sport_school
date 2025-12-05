from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.coach.models import Coach
from app.user.schemas import UserSchema
from app.middleware import get_current_user
from sqlalchemy import select
from app.specialization.models import SportType, CoachSportType  # Импортируем модели
from app.utils import get_password_hash
from app.training.models import Training
from datetime import date, datetime
from app.hall.models import Hall
from app.training_hall.models import TrainingHall
from app.athlete.models import Athlete
from app.user.models import User
from app.group.models import Group


test_router = APIRouter(prefix="/tests", tags=["СОЗДАТЬ ТЕСТОВЫЕ ДАННЫЕ"])

@test_router.post("/coaches", summary="Заполнение базы данных тестовыми данными о тренерах")
async def seed_coaches():
    async with async_session_maker() as session:
        # Флаги для отслеживания, какие данные нужно добавить
        add_sport_types = False
        add_coaches = False
        add_coach_sport_types = False

        # Проверяем, есть ли уже типы спорта в базе данных
        existing_sport_types = await session.execute(select(SportType))
        if existing_sport_types.scalars().first() is None:
            add_sport_types = True
            print("Типов спорта нет в базе данных, добавляем...")
        else:
            print("Типы спорта уже существуют в базе данных.")

        # Проверяем, есть ли уже тренеры в базе данных
        existing_coaches = await session.execute(select(Coach))
        if existing_coaches.scalars().first() is None:
            add_coaches = True
            print("Тренеров нет в базе данных, добавляем...")
        else:
            print("Тренеры уже существуют в базе данных.")

        # Проверяем, есть ли уже CoachSportType в базе данных
        existing_coach_sport_types = await session.execute(select(CoachSportType))
        if existing_coach_sport_types.scalars().first() is None:
            add_coach_sport_types = True
            print("CoachSportType нет в базе данных, добавляем...")
        else:
            print("CoachSportType уже существуют в базе данных.")

        # Создаем данные для SportType, если нужно
        sport_types_data = []
        if add_sport_types:
            sport_types_data = [
                {"name": "Плавание", "description": "Отработка техники плавания, развитие выносливости и укрепление всех групп мышц. Занятия для разных возрастных групп и уровней подготовки"},
                {"name": "Борьба", "description": "Изучение техник единоборств, развитие силы, ловкости и координации. Тренировки включают работу в партере и стойке"},
                {"name": "Легкая атлетика", "description": "Развитие скорости, выносливости и координации. Беговые дисциплины, прыжки, метания"},
                {"name": "Тяжелая атлетика", "description": "Совершенствование техники выполнения упражнений со штангой. Развитие взрывной силы и мышечной массы"},
                {"name": "Гимнастика", "description": "Развитие гибкости, силы и координации. Спортивная и художественная гимнастика для детей и взрослых"},
                {"name": "Теннис", "description": "Обучение технике ударов, тактике игры. Индивидуальные и групповые занятия на корте"},
                {"name": "Баскетбол", "description": "Командные тренировки, отработка бросков, дриблинга и тактических комбинаций"},
                {"name": "Футбол", "description": "Техника владения мячом, тактические построения, командная игра. Занятия для разных возрастных групп"},
                {"name": "Волейбол", "description": "Обучение технике подач, пасов и атакующих ударов. Командные и индивидуальные тренировки"},
                {"name": "Бокс", "description": "Освоение ударной техники, работа над скоростью и реакцией. Тренировки на снарядах и в спаррингах"},
                {"name": "Йога", "description": "Практика асан, дыхательных упражнений и медитации. Улучшение гибкости и снятие стресса"},
                {"name": "Кроссфит", "description": "Высокоинтенсивные функциональные тренировки, развивающие все физические качества"},
                {"name": "Стретчинг", "description": "Упражнения на развитие гибкости и мобильности суставов. Подходит для любого уровня подготовки"},
                {"name": "Аэробика", "description": "Кардиотренировки под музыку, направленные на развитие выносливости и снижение веса"},
                {"name": "Скалолазание", "description": "Техника лазания, развитие силы хвата и координации. Тренировки на искусственном рельефе"},
                {"name": "Бодибилдинг", "description": "Набор мышечной массы и формирование пропорционального тела."}
            ]

        for sport_type_data in sport_types_data:
            sport_type = SportType(**sport_type_data)
            session.add(sport_type)
        await session.flush() # Flush чтобы получить id sport_type
        print("Sport types added")

        # Создаем данные для Coach, если нужно
        coaches_data = []
        if add_coaches:
            coaches_data = [
                {"experience_years": 8, "bio": "Специалист по функциональному тренингу и коррекции осанки", "full_name": "Иванова Анна Сергеевна", "password_hash": get_password_hash("password"), "phone_number": "+79991112233", "email": "ivanova@example.com"},
                {"experience_years": 15, "bio": "Мастер-тренер по бодибилдингу, чемпион региона", "full_name": "Петров Дмитрий Игоревич", "password_hash": get_password_hash("password"), "phone_number": "+79991112234", "email": "petrov@example.com"},
                {"experience_years": 5, "bio": "Эксперт по йоге и пилатесу для восстановления", "full_name": "Сидорова Екатерина Владимировна", "password_hash": get_password_hash("password"), "phone_number": "+79991112235", "email": "sidorova@example.com"},
                {"experience_years": 20, "bio": "Ветеран фитнес-индустрии, специалист по реабилитации", "full_name": "Козлов Александр Николаевич", "password_hash": get_password_hash("password"), "phone_number": "+79991112236", "email": "kozlov@example.com"},
                {"experience_years": 3, "bio": "Молодой специалист по кроссфиту и HIIT тренировкам", "full_name": "Морозова Ольга Дмитриевна", "password_hash": get_password_hash("password"), "phone_number": "+79991112237", "email": "morozova@example.com"},
                {"experience_years": 10, "bio": "Сертифицированный тренер по плаванию и аквааэробике", "full_name": "Никитин Сергей Петрович", "password_hash": get_password_hash("password"), "phone_number": "+79991112238", "email": "nikitin@example.com"},
                {"experience_years": 7, "bio": "Специалист по питанию и силовым тренировкам для женщин", "full_name": "Волкова Марина Алексеевна", "password_hash": get_password_hash("password"), "phone_number": "+79991112239", "email": "volkova@example.com"},
                {"experience_years": 12, "bio": "Эксперт по боевым искусствам и самообороне", "full_name": "Орлов Андрей Викторович", "password_hash": get_password_hash("password"), "phone_number": "+79991112240", "email": "orlov@example.com"},
                {"experience_years": 6, "bio": "Тренер по стретчингу и мобильности суставов", "full_name": "Лебедева Ирина Олеговна", "password_hash": get_password_hash("password"), "phone_number": "+79991112241", "email": "lebedeva@example.com"},
                {"experience_years": 9, "bio": "Специалист по тренировкам для старшего возраста", "full_name": "Семенов Павел Геннадьевич", "password_hash": get_password_hash("password"), "phone_number": "+79991112242", "email": "semenov@example.com"},
            ]
            
        for coach_data in coaches_data:
            coach = Coach(**coach_data)
            session.add(coach)
        await session.flush() # Flush чтобы получить id coach
        print("Coaches added")
        await session.commit()

        # Создаем связи между тренерами и типами спорта, если нужно
        if add_coach_sport_types:
            #  Создаем связи между тренерами и типами спорта
            #  Здесь нужно указать, какие специализации у каких тренеров

            # Получаем id SportType
            sport_types = await session.execute(select(SportType))
            sport_types_dict = {sport_type.name: sport_type.id for sport_type in sport_types.scalars().all()}
            print(f"sport_types_dict: {sport_types_dict}")

            # Связываем тренеров со специализациями
            #  Предполагаем что  Иванова Анна Сергеевна - Плавание, Йога
            #  Петров Дмитрий Игоревич - Бодибилдинг
            #  Сидорова Екатерина Владимировна - Йога, Стретчинг
            #  Козлов Александр Николаевич - Стретчинг, Йога
            #  Морозова Ольга Дмитриевна - Кроссфит, Аэробика
            #  Никитин Сергей Петрович - Плавание
            #  Волкова Марина Алексеевна - Тяжелая атлетика
            #  Орлов Андрей Викторович - Бокс, Борьба
            #  Лебедева Ирина Олеговна - Стретчинг, Йога
            #  Семенов Павел Геннадьевич - Йога

            coach_specializations = {
                "Иванова Анна Сергеевна": ["Плавание", "Йога"],
                "Петров Дмитрий Игоревич": ["Бодибилдинг"],
                "Сидорова Екатерина Владимировна": ["Йога", "Стретчинг"],
                "Козлов Александр Николаевич": ["Стретчинг", "Йога"],
                "Морозова Ольга Дмитриевна": ["Кроссфит", "Аэробика"],
                "Никитин Сергей Петрович": ["Плавание"],
                "Волкова Марина Алексеевна": ["Тяжелая атлетика"],
                "Орлов Андрей Викторович": ["Бокс", "Борьба"],
                "Лебедева Ирина Олеговна": ["Стретчинг", "Йога"],
                "Семенов Павел Геннадьевич": ["Йога"],
            }

            coaches = await session.execute(select(Coach))
            coaches_dict = {coach.full_name: coach.id for coach in coaches.scalars().all()}
            print(f"coaches_dict: {coaches_dict}")

            for coach_name, specialization_names in coach_specializations.items():
                coach_id = next((coach_id for coach_name_temp, coach_id in coaches_dict.items() if coach_name_temp == coach_name), None)
                print(f"coach_name: {coach_name}, coach_id: {coach_id}")
                if coach_id:
                    for specialization_name in specialization_names:
                        sport_type_id = sport_types_dict.get(specialization_name)
                        print(f"specialization_name: {specialization_name}, sport_type_id: {sport_type_id}")
                        if sport_type_id:
                            coach_sport_type = CoachSportType(coach_id=coach_id, sport_type_id=sport_type_id)
                            session.add(coach_sport_type)
            await session.commit()
            print("Coach sport types added")
        else:
            print("Coach sport types already exist, skipping...")

    return {"message": "Тестовые данные успешно добавлены"}


@test_router.post("/halls_and_trainings", summary="Заполнение базы данных тестовыми данными о залах и тренировках, и связях между ними")
async def seed_halls_and_trainings():
    async with async_session_maker() as session:
        # Проверяем, есть ли уже залы в базе данных
        existing_halls = await session.execute(select(Hall))
        if existing_halls.scalars().first() is not None:
            print("Тестовые данные о залах уже существуют в базе данных.")
            #return {"message": "Тестовые данные о залах уже существуют в базе данных."} # Don't return, just skip hall creation
            add_halls = False
        else:
            add_halls = True

        # Проверяем, есть ли уже тренировки в базе данных
        existing_trainings = await session.execute(select(Training))
        if existing_trainings.scalars().first() is not None:
            print("Тестовые данные о тренировках уже существуют в базе данных.")
            #return {"message": "Тестовые данные о тренировках уже существуют в базе данных."} # Don't return, just skip training creation
            add_trainings = False
        else:
            add_trainings = True

        halls_data = []
        if add_halls:
             halls_data = [
                {"name": "Зал бокса", "capacity": 20},
                {"name": "Бассейн 1", "capacity": 30},
                {"name": "Зал №2", "capacity": 50},
                {"name": "Кроссфит зона", "capacity": 40},
            ]

        halls = []
        for hall_data in halls_data:
            hall = Hall(**hall_data)
            session.add(hall)
            halls.append(hall)
        await session.flush()

        trainings_data = []
        if add_trainings:
            # Создаем тестовые данные для тренировок
            #{"type": "individual", "title": "Анализ техники плавания", "coach_id": coaches[0].id, "time": "09:00 - 10:30", "location": "Бассейн 1", "date": date(2024, 5, 25), "participants": None},
            trainings_data = [
                {"start_time": datetime(2024, 5, 25, 9, 0), "end_time": datetime(2024, 5, 25, 10, 30), "is_group_training": False},
                {"start_time": datetime(2024, 5, 25, 11, 0), "end_time": datetime(2024, 5, 25, 12, 30), "is_group_training": True},
                {"start_time": datetime(2024, 5, 26, 14, 0), "end_time": datetime(2024, 5, 26, 15, 0), "is_group_training": False},
                {"start_time": datetime(2024, 5, 26, 16, 0), "end_time": datetime(2024, 5, 26, 17, 30), "is_group_training": True},
            ]
            
        trainings = []
        for training_data in trainings_data:
            training = Training(**training_data)
            session.add(training)
            trainings.append(training)
        await session.flush()

        training_halls_data = []

        # Create the relationships between trainings and halls
        if add_trainings and add_halls:
            training_halls_data = [
                {"training_id": trainings[0].id, "hall_id": halls[1].id}, # Swimming analysis in Pool 1
                {"training_id": trainings[1].id, "hall_id": halls[2].id}, # OFP in Hall 2
                {"training_id": trainings[2].id, "hall_id": halls[0].id}, # Boxing in Boxing hall
                {"training_id": trainings[3].id, "hall_id": halls[3].id}, # Functional training in CrossFit zone
            ]

        for training_hall_data in training_halls_data:
            training_hall = TrainingHall(**training_hall_data)
            session.add(training_hall)

        await session.commit()
        print("Тестовые данные о залах и тренировках успешно добавлены")
        return {"message": "Тестовые данные о залах и тренировках успешно добавлены"}


@test_router.post("/athletes", summary="Заполнение базы данных тестовыми данными об атлетах")
async def seed_athletes():
    async with async_session_maker() as session:
        # Проверяем, есть ли уже атлеты в базе данных
        existing_athletes = await session.execute(select(Athlete))
        if existing_athletes.scalars().first() is not None:
            print("Тестовые данные об атлетах уже существуют в базе данных.")
            return {"message": "Тестовые данные об атлетах уже существуют в базе данных."}

        athletes_data = [
            {"full_name": "Иван Иванов", "phone_number": "+79001234567", "email": "ivan@example.com", "password_hash": get_password_hash("password")},
            {"full_name": "Петр Петров", "phone_number": "+79001234568", "email": "petr@example.com", "password_hash": get_password_hash("password")},
            {"full_name": "Сидор Сидоров", "phone_number": "+79001234569", "email": "sidor@example.com", "password_hash": get_password_hash("password")},
        ]

        for athlete_data in athletes_data:
            athlete = Athlete(
                full_name=athlete_data["full_name"],
                phone_number=athlete_data["phone_number"],
                email=athlete_data["email"],
                password_hash=athlete_data["password_hash"],
            )
            session.add(athlete)

        await session.commit()
        print("Тестовые данные об атлетах успешно добавлены")
        return {"message": "Тестовые данные об атлетах успешно добавлены"}


@test_router.post("/groups", summary="Заполнение базы данных тестовыми данными о группах")
async def seed_groups():
    pass