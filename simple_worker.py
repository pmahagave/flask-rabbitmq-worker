import pika
import json
import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'items.db')

def process_item(item_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET status = 'completed' WHERE rowid = (SELECT rowid FROM items WHERE item = ? AND status = 'pending' LIMIT 1)",
        (item_name,)
    )
    conn.commit()
    conn.close()
    print(f"Item '{item_name}' marked as completed")

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    data = json.loads(message)
    item_name = data.get('item')
    print(f" Received: {item_name}")
    process_item(item_name)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672)
    )
    channel = connection.channel()
    channel.queue_declare(queue='item_queue', durable=True)
    channel.basic_consume(queue='item_queue', on_message_callback=callback, auto_ack=False)
    print(" Waiting for messages... (Press CTRL+C to stop)")
    channel.start_consuming()

if __name__ == '__main__':
    print("Starting Simple Worker...")
    start_worker()