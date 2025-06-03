import asyncio
import json
import os
from contextlib import asynccontextmanager
from threading import Thread
import dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.database import get_db_session
from modules.tasks.router import router as router_tasks
from modules.ai_models.router import router as router_models
from modules.auth.router import router as router_auth
from modules.pages.router import router as router_pages
from modules.primitive_predictions import schema as primitive_prediction_schema
from modules.primitive_predictions.dao import post_primitive_predictions
from modules.primitive_class.dao import get_primitive_class_id
from modules.scene_class_predictions import schema as scene_class_prediction_schema
from modules.scene_class_predictions.dao import post_scene_class_predictions
from modules.scene_class.dao import get_scene_class_id
from modules.tasks.dao import update_task_status, update_task_scene_class, get_task_models
from modules.ai_models.dao import get_detection_models, get_classification_models

import modules.server_producer as sp
from modules.server_consumer import get_consumer


dotenv.load_dotenv()

TASK_ID_BYTE_SIZE = int(os.getenv("TASK_ID_BYTE_SIZE"))
D_MODEL_ID_BYTE_SIZE = int(os.getenv("D_MODEL_ID_BYTE_SIZE"))
C_MODEL_ID_BYTE_SIZE = int(os.getenv("C_MODEL_ID_BYTE_SIZE"))

init_db = True

classification_models = {1: "GRU_model_v1",
                         2: "GRU_model_v2_binary"}
detection_models = {1: "YOLOv11m-obb"}

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
                    msg_value = msg.value()
                    task_id, d_model_id, c_model_id, result = (int.from_bytes(msg_value[0:TASK_ID_BYTE_SIZE]),
                                                               int.from_bytes(msg_value[TASK_ID_BYTE_SIZE:D_MODEL_ID_BYTE_SIZE]),
                                                               int.from_bytes(msg_value[TASK_ID_BYTE_SIZE+D_MODEL_ID_BYTE_SIZE:TASK_ID_BYTE_SIZE+D_MODEL_ID_BYTE_SIZE+C_MODEL_ID_BYTE_SIZE]),
                                                               (msg_value[TASK_ID_BYTE_SIZE+D_MODEL_ID_BYTE_SIZE+C_MODEL_ID_BYTE_SIZE:]).decode("utf-8"))

                    # Загрузка результата в БД по айди задачи
                    primitive_result_dicts = json.loads(result)
    
                    async def load_primitive_predictions():
                        async with get_db_session() as ses:
                            preds = [
                                primitive_prediction_schema.PrimitivePredictionCreate(
                                    task_id=task_id,
                                    primitive_class_id=(await get_primitive_class_id(db=ses, primitive_class=pred["class_name"])).id,
                                    x1_coord=pred["x1_coord"],
                                    y1_coord=pred["y1_coord"],
                                    x2_coord=pred["x2_coord"],
                                    y2_coord=pred["y2_coord"],
                                    x3_coord=pred["x3_coord"],
                                    y3_coord=pred["y3_coord"],
                                    x4_coord=pred["x4_coord"],
                                    y4_coord=pred["y4_coord"],
                                    probability=pred["probability"]
                                ) for pred in primitive_result_dicts]

                            await post_primitive_predictions(db=ses, predictions=preds)

                    asyncio.ensure_future(load_primitive_predictions(), loop=main_loop)

                    # Выбор модели классификации по айди модели в задаче
                    task_cl_model = classification_models[c_model_id]

                    if task_cl_model == "GRU_model_v1":
                        # Вызов классификации мультиклассовой моделью
                        await sp.dispatch_task_classify_image(task_id=task_id.to_bytes(TASK_ID_BYTE_SIZE),
                                                              d_model_id=d_model_id.to_bytes(D_MODEL_ID_BYTE_SIZE),
                                                              c_model_id=c_model_id.to_bytes(C_MODEL_ID_BYTE_SIZE),
                                                              primitives=json.dumps(primitive_result_dicts).encode('utf-8'),
                                                              loop=asyncio.get_event_loop())

                    elif task_cl_model == "GRU_model_v2_binary":
                        # Вызов классификации ансамблем бинарных моделей
                        await sp.dispatch_task_classify_binary_image(task_id=task_id.to_bytes(TASK_ID_BYTE_SIZE),
                                                                     d_model_id=d_model_id.to_bytes(D_MODEL_ID_BYTE_SIZE),
                                                                     c_model_id=c_model_id.to_bytes(C_MODEL_ID_BYTE_SIZE),
                                                                     primitives=json.dumps(primitive_result_dicts).encode('utf-8'),
                                                                     loop=asyncio.get_event_loop())
                    else:
                        print(f"Classification model with id '{c_model_id}' does not exist, task cannot be processed.")

                        async def task_status_update():
                            async with get_db_session() as ses:
                                # status_id 3 = done
                                await update_task_status(db=ses, task_id=task_id, new_status_id=3)

                        asyncio.ensure_future(task_status_update(), loop=main_loop)

                # Обработка результатов классификации
                elif msg.topic() == "classified-image":
                    # Получаем айди задачи и результат
                    msg_value = msg.value()
                    task_id, d_model_id, c_model_id, result = (int.from_bytes(msg_value[0:TASK_ID_BYTE_SIZE]),
                                                               int.from_bytes(msg_value[TASK_ID_BYTE_SIZE:D_MODEL_ID_BYTE_SIZE]),
                                                               int.from_bytes(msg_value[TASK_ID_BYTE_SIZE + D_MODEL_ID_BYTE_SIZE:C_MODEL_ID_BYTE_SIZE]),
                                                               (msg_value[TASK_ID_BYTE_SIZE + D_MODEL_ID_BYTE_SIZE + C_MODEL_ID_BYTE_SIZE:]).decode("utf-8"))

                    # Загрузка результата в БД по айди задачи
                    class_result_dicts = json.loads(result)

                    async def load_scene_class_predictions():
                        async with get_db_session() as ses:
                            class_preds = []
                            for i, scene_class in enumerate(class_result_dicts["classes"].values()):
                                class_preds.append(
                                    scene_class_prediction_schema.SceneClassPredictionCreate(
                                        task_id=task_id,
                                        scene_class_id=(await get_scene_class_id(db=ses, scene_class=scene_class)).id,
                                        scene_class_prob=class_result_dicts["class_probs"][i]
                                    )
                                )
                            await post_scene_class_predictions(db=ses, predictions=class_preds)

                    asyncio.ensure_future(load_scene_class_predictions(), loop=main_loop)
                    # Обновление статуса и топ класса сцены задачи
                    async def load_task_updates():
                        async with get_db_session() as ses:
                            # status_id 3 = done
                            await update_task_status(db=ses, task_id=task_id, new_status_id=3)
                            class_id = (await get_scene_class_id(db=ses, scene_class=class_result_dicts["top_class_name"])).id
                            await update_task_scene_class(db=ses, task_id=task_id, new_scene_class_id=class_id)
                    asyncio.ensure_future(load_task_updates(), loop=main_loop)

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    current_loop = asyncio.get_running_loop()
    consumer_thread = Thread(target=lambda: asyncio.run(server_consumer(current_loop)))
    consumer_thread.start()

    yield
    sp.close_producer()


app = FastAPI(lifespan=lifespan)

app.include_router(router_pages)

app.include_router(router_tasks)

app.include_router(router_models)

app.include_router(router_auth)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)


# RUN
# fastapi run src/app/main.py