import os
import dotenv

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from .db_models.models import Tasks, Status, SceneClass, PrimitiveClass, DetectionModels, ClassificationModels, PrimitivePredictions, Users

dotenv.load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_NAME")

# Sync DB
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# engine = create_engine(DATABASE_URL)
# session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)
#
#
# def get_db():
#     db = session_maker()
#     try:
#         yield db
#     finally:
#         db.close()

# Async DB
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=True)
session_maker = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with session_maker() as session:
        yield session

def get_db_session():
    return session_maker()

# Словарь классов сцен
dbSceneClasses = [
    SceneClass(
        scene_class="office"),
    SceneClass(
        scene_class="beach"),
    SceneClass(
        scene_class="street")
]

# Словарь классов примитивов
dbPrimitiveClasses = [
    PrimitiveClass(
        primitive_class="cuboid"),
    PrimitiveClass(
        primitive_class="sphere"),
    PrimitiveClass(
        primitive_class="pyramid"),
    PrimitiveClass(
        primitive_class="torus"),
    PrimitiveClass(
        primitive_class="cylinder")
]

# Словарь статусов
dbStatuses = [
    Status(status="queued"),
    Status(status="in progress"),
    Status(status="done")
]

# Словарь моделей детекции
dbDModels = [
    DetectionModels(name="YOLO"),
    DetectionModels(name="SSD"),
    ClassificationModels(name="model_v1"),
]

# Тестовые данные
dbUsers = [
    Users(username="first",
        hashed_password="$2b$12$SmZBPfFaw78FguMgRarX5e1iKckloh6Pi/3Q1ZSGuOzC345gHRL8C"), # 111
    Users(username="second",
        hashed_password="$2b$12$n8evGhlqi4pJHmiykHfFzuEqPnE2qLhl1apdj9/.D8cbHCGZmTejO"), # 222
]

dbTasks = [
    Tasks(
        owner_id=1,
        # created_at="2024-04-25T18:25:43.511Z",
        scene_class_id=1,
        detection_model_id=1,
        classification_model_id=1,
        status_id=3,
        input_path="img_1.png"
    ),
    Tasks(
        owner_id=1,
        # created_at="2024-04-25T18:25:43.511Z",
        scene_class_id=None,
        detection_model_id=2,
        classification_model_id=1,
        status_id=1,
        input_path="img_2.png"
    ),
    Tasks(
        owner_id=1,
        # created_at="2024-04-25T18:25:43.511Z",
        scene_class_id=None,
        detection_model_id=1,
        classification_model_id=1,
        status_id=2,
        input_path="img_3.png"
    ),
    Tasks(
        owner_id=2,
        # created_at="2024-04-25T18:25:43.511Z",
        scene_class_id=1,
        detection_model_id=1,
        classification_model_id=1,
        status_id=3,
        input_path="img_4.png"
    )
]

dbPredictions = [
    PrimitivePredictions(
        task_id=1,
        primitive_class_id=1,
        x1_coord=0.1,
        y1_coord=0.1,
        x2_coord=0.2,
        y2_coord=0.2,
        x3_coord=0.3,
        y3_coord=0.3,
        x4_coord=0.4,
        y4_coord=0.4,
        probability=0.8
    ),
    PrimitivePredictions(
        task_id=1,
        primitive_class_id=2,
        x1_coord=0.1,
        y1_coord=0.1,
        x2_coord=0.2,
        y2_coord=0.2,
        x3_coord=0.3,
        y3_coord=0.3,
        x4_coord=0.4,
        y4_coord=0.4,
        probability=0.88
    ),
    PrimitivePredictions(
        task_id=1,
        primitive_class_id=3,
        x1_coord=0.2,
        y1_coord=0.2,
        x2_coord=0.3,
        y2_coord=0.3,
        x3_coord=0.4,
        y3_coord=0.4,
        x4_coord=0.5,
        y4_coord=0.5,
        probability=0.85
    ),
    PrimitivePredictions(
        task_id=4,
        primitive_class_id=3,
        x1_coord=0.3,
        y1_coord=0.3,
        x2_coord=0.4,
        y2_coord=0.4,
        x3_coord=0.5,
        y3_coord=0.5,
        x4_coord=0.6,
        y4_coord=0.6,
        probability=0.28
    ),
]


async def init_data():
    # Заполнение словарей
    async with session_maker() as session:
        try:
            for scene in dbSceneClasses:
                session.add(scene)
                await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

    async with session_maker() as session:
        try:
            for primitive in dbPrimitiveClasses:
                session.add(primitive)
                await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

    async with session_maker() as session:
        try:
            for status in dbStatuses:
                session.add(status)
                await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

    async with session_maker() as session:
        try:
            for model in dbDModels:
                session.add(model)
                await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


    # Заполнение тестовых данных
    # Добавление пользователей должно следовать перед добавлением задач
    async with session_maker() as session:
        try:
            for user in dbUsers:
                session.add(user)
                await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

    async with session_maker() as session:
        try:
            for task in dbTasks:
                session.add(task)
                await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

    async with session_maker() as session:
        try:
            for pred in dbPredictions:
                session.add(pred)
                await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
