import os
import dotenv

from confluent_kafka import Consumer

dotenv.load_dotenv("../../task_service/.env")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

config = {
    # User-specific properties that you must set
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,

    # Fixed properties
    'group.id': 'detection-model',
    'auto.offset.reset': 'earliest',
    'fetch.message.max.bytes': 52428800
}

# Create Consumer instance
consumer = Consumer(config)

# Топик для задач, требующих детекцию примитивов моделью детекции
topic_detect_primitives = "detect-primitives"

consumer.subscribe([topic_detect_primitives])

def get_consumer():
    return consumer