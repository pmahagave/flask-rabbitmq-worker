import sqlite3
from celery import Celery
from app.config import Config

celery = Celery('worker', broker=Config.CELERY_BROKER_URL)

celery.conf.task_routes = {
    'process_item': {'queue': 'item_queue'},
}

celery.conf.task_default_queue = 'item_queue'

celery.conf.worker_prefetch_multiplier = 1

@celery.task(name='process_item', queue='item_queue')
def process_item(item_data):
    item_name = item_data['item']
    
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE items SET status = 'completed' WHERE rowid = (SELECT rowid FROM items WHERE item = ? AND status = 'pending' LIMIT 1)",
        (item_name,)
    )
    
    conn.commit()
    conn.close()
    return f"Processed item: {item_name}"