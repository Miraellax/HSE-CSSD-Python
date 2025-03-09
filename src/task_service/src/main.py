import ast
import asyncio
import json
import os

from contextlib import asynccontextmanager
from threading import Thread

import dotenv
import uvicorn
from fastapi import FastAPI

from modules.database import engine, init_data, get_db_session
from modules.db_models.models import Base
from modules.tasks.router import router as router_tasks
from modules.ai_models.router import router as router_models
from modules.auth.router import router as router_auth

import modules.server_producer as sp
from src.task_service.src.modules.predictions import schema as prediction_schema
from src.task_service.src.modules.predictions.dao import post_predictions
from src.task_service.src.modules.server_consumer import get_consumer

dotenv.load_dotenv()

TASK_ID_BYTE_SIZE = int(os.getenv("TASK_ID_BYTE_SIZE"))

init_db = True


async def server_consumer(main_loop):
    consumer = get_consumer()

    try:
        while True:
            msg = consumer.poll(10.0)
            if msg is None:
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                print("Consumed event from topic {topic}.".format(topic=msg.topic()))

                # Обработка результатов детекции
                if msg.topic() == "detected-primitives":
                    # Получаем айди задачи и результат
                    task_id, result = int.from_bytes(msg.value()[0:TASK_ID_BYTE_SIZE]), (msg.value()[TASK_ID_BYTE_SIZE:]).decode("utf-8")
                    print(f"SERVER GOT DETECTION MODEL RESULT for task_id({task_id}):", result)

                    # Загрузка результата в БД по айди задачи
                    result_dicts = json.loads(result)
                    print(result_dicts)
                    preds = [
                        prediction_schema.PredictionCreate(
                            task_id=task_id,
                            primitive_class_id=pred["class_id"],
                            x_coord=pred["x_coord"],
                            y_coord=pred["y_coord"],
                            width=pred["width"],
                            height=pred["height"],
                            rotation=pred["rotation"],
                            probability=pred["probability"]
                    ) for pred in result_dicts]
    
                    async def load_predictions():
                        async with get_db_session() as ses:
                            await post_predictions(db=ses, predictions=preds)

                    asyncio.ensure_future(load_predictions(), loop=main_loop)
                    # TODO вызывать классификацию

                # TODO Обработка результатов классификации
                elif msg.topic() == "classified-image":
                    # Получаем айди задачи и результат
                    task_id, result_bytes = msg.value()[0:TASK_ID_BYTE_SIZE], msg.value()[TASK_ID_BYTE_SIZE:]
                    print(f"SERVER GOT CLASSIFICATION MODEL RESULT for task_id({int.from_bytes(task_id)}):",
                          result_bytes.decode("utf-8"))

                    # TODO загрузить результаты классов для задачи в БД, обновить статус задачи на "сделано"

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if init_db:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await init_data()

    current_loop = asyncio.get_running_loop()
    consumer_thread = Thread(target=lambda: asyncio.run(server_consumer(current_loop)))
    consumer_thread.start()

    yield
    sp.close_producer()


app = FastAPI(lifespan=lifespan)

app.include_router(router_tasks)

app.include_router(router_models)

app.include_router(router_auth)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)


# RUN
# fastapi run src/app/main.py