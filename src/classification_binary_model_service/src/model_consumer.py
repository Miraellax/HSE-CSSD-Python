import os
import dotenv

from confluent_kafka import Consumer

dotenv.load_dotenv("../../task_service/.env")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

config = {
    # User-specific properties that you must set
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,

    # Fixed properties
    'group.id': 'classification-binary-model',
    'auto.offset.reset': 'earliest'
}

# Create Consumer instance
consumer = Consumer(config)

# Топик для задач, требующих детекцию примитивов моделью детекции
topic_classify_binary_image = "classify-binary-image"

consumer.subscribe([topic_classify_binary_image])

def get_consumer():
    return consumer