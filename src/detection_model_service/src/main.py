import asyncio
import json
import os

import dotenv

from model_consumer import get_consumer
from ai_model.ai_model import process
from src.detection_model_service.src.model_producer import dispatch_task_detected_primitives

dotenv.load_dotenv("../../task_service/.env")

TASK_ID_BYTE_SIZE = int(os.getenv("TASK_ID_BYTE_SIZE"))

async def main():
    consumer = get_consumer()

    try:
        while True:
            msg = consumer.poll(10.0)
            if msg is None:
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                print("Consumed event from topic {topic}.".format(topic=msg.topic()))

                # Получаем айди задачи для отправки результата обратно и изображение для обработки
                task_id, image_bytes = msg.value()[0:TASK_ID_BYTE_SIZE], msg.value()[TASK_ID_BYTE_SIZE:]

                # Обработка изображения
                result = await process(image_bytes)
                print(f"DETECTION MODEL RESULT for task_id({int.from_bytes(task_id)}):", result)

                # Отправка результата обратно на сервер
                answ = await dispatch_task_detected_primitives(task_id=task_id, result=json.dumps(result).encode("utf-8"), loop=asyncio.get_event_loop())
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()

asyncio.run(main())