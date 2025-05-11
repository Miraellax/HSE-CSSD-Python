import asyncio
import json
import os

import dotenv

from model_consumer import get_consumer
from ai_model import ai_model
from model_producer import dispatch_task_classified_image

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

                # Get task id to send result back and get image to predict
                task_id, primitives_bytes = msg.value()[0:TASK_ID_BYTE_SIZE], msg.value()[TASK_ID_BYTE_SIZE:]
                primitives = json.loads(primitives_bytes.decode('utf-8'))

                # Process image
                result = await ai_model.process(primitives)
                print(f"Classification model RESULT for task_id({int.from_bytes(task_id)}):", result)

                # Send resulting primitives to server
                answ = await dispatch_task_classified_image(task_id=task_id,
                                                               result=json.dumps(result).encode("utf-8"),
                                                               loop=asyncio.get_event_loop())
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()

asyncio.run(main())