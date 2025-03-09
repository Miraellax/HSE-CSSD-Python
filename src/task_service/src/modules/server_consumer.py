import os
import dotenv

from confluent_kafka import Consumer

dotenv.load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

config = {
    # User-specific properties that you must set
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,

    # Fixed properties
    'group.id': 'server',
    'auto.offset.reset': 'earliest'
}

# Create Consumer instance
consumer = Consumer(config)

# Топик для задач с результатами детекции примитивов от модели детекции
topic_detected_primitives = "detected-primitives"

# Топик для задач с результатами классификации изображения от модели классификации
topic_classified_image = "classified-image"

consumer.subscribe([topic_detected_primitives, topic_classified_image])

def get_consumer():
    return consumer