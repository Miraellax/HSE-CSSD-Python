import asyncio
import os
import dotenv

from threading import Thread
from confluent_kafka import Producer, KafkaException


# https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/asyncio_example.py
class AsyncProducer:
    def __init__(self, configs):
        self._producer = Producer(configs)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self):
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic, value, loop):
        """
        An awaitable produce method.
        """
        result = loop.create_future()

        def delivery_callback(err, msg):
            if err:
                loop.call_soon_threadsafe(result.set_exception, KafkaException(err))
            elif msg.error():
                loop.call_soon_threadsafe(result.set_exception, KafkaException(msg.error()))
            else:
                loop.call_soon_threadsafe(result.set_result, msg)

        self._producer.produce(topic, value, on_delivery=delivery_callback)
        return result


dotenv.load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,

        # Fixed properties
        'acks': 'all'
    }


producer = AsyncProducer(configs=config)

def close_producer():
    producer.close()

# Топик для задач с результатами детекции примитивов от модели детекции
topic_detected_primitives = "detected-primitives"

# task_id length = .env/TASK_ID_BYTE_SIZE
async def dispatch_task_detected_primitives(task_id: bytes, d_model_id:bytes, c_model_id:bytes, result: bytes, loop):
    result = await producer.produce(topic=topic_detected_primitives, value=task_id + d_model_id + c_model_id + result, loop=loop)
    return result


