import os

class Config:
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'items.db')
    RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', 5672))
    RABBITMQ_QUEUE = 'item_queue'
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'