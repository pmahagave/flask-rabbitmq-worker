import pika
import json
import sqlite3
from flask import Blueprint, request, jsonify
from .config import Config

bp = Blueprint('producer', __name__)

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    return conn

# ============ POST ENDPOINT ============
@bp.route('/items', methods=['POST'])
def create_item():
    print("🔍 Request received!")
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data'}), 400
        
        item_name = data.get('item')
        if not item_name:
            return jsonify({'error': 'item is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (status, item) VALUES (?, ?)",
            ('pending', item_name)
        )
        conn.commit()
        conn.close()
        print(f"💾 Inserted: {item_name}")
        
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=Config.RABBITMQ_HOST, port=Config.RABBITMQ_PORT)
        )
        channel = connection.channel()
        channel.queue_declare(queue=Config.RABBITMQ_QUEUE, durable=True)
        
        message = json.dumps({'item': item_name})
        channel.basic_publish(
            exchange='',
            routing_key=Config.RABBITMQ_QUEUE,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
        print(f" Sent to RabbitMQ: {message}")
        
        return jsonify({
            'message': 'Item received and queued',
            'item': item_name,
            'status': 'pending'
        }), 202
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# ============ GET ENDPOINT ============
@bp.route('/items', methods=['GET'])
def get_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        conn.close()
        print(f" Items: {items}")
        return jsonify({'items': items}), 200
    except Exception as e:
        print(f"GET Error: {e}")
        return jsonify({'error': str(e)}), 500