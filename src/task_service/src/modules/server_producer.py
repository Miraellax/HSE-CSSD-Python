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
            self._producer.poll(2.0)

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
        'message.max.bytes': 52428800,
        # Fixed properties
        'acks': 'all'
    }


producer = AsyncProducer(configs=config)

def close_producer():
    producer.close()

# Топик для задач, требующих детекцию примитивов моделью детекции
topic_detect_primitives = "detect-primitives"

# Топик для задач, требующих классификацию изображения моделью классификации
topic_classify_image = "classify-image"

# Топик для задач с результатами детекции примитивов от модели детекции
topic_detected_primitives = "detected-primitives"

# Топик для задач с результатами классификации изображения от модели классификации
topic_classified_image = "classified-image"

async def dispatch_task_detect_primitives(task_id: bytes, image: bytes, loop):
    try:
        result = await producer.produce(topic=topic_detect_primitives, value=task_id+image, loop=loop)
    except Exception as e:
        print(e)
    return result

async def dispatch_task_classify_image(task_id:bytes, primitives: bytes, loop):
    result = await producer.produce(topic=topic_classify_image, value=task_id+primitives, loop=loop)
    return result


