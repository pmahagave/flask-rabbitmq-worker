# Flask-RabbitMQ-Celery Project

## Prerequisites
- Python 3.9+
- RabbitMQ Server running on localhost:5672

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start RabbitMQ:
```bash
# On Windows
rabbitmq-server

# On Linux/Mac
rabbitmq-server
```

## Running the Project

1. Start the Flask application:
```bash
python run.py
```
The API will be available at http://localhost:5000

2. Start the Celery worker in a separate terminal:
```bash
celery -A celery_worker worker --loglevel=info -Q item_queue
```

## API Endpoints

### POST /api/items
Create a new item (sends to RabbitMQ for async processing)

**Request:**
```json
{
    "item": "book"
}
```

**Response:** 202 Accepted

---

### GET /api/delay?delay_value=N
Make 5 concurrent HTTP requests to httpbin.org

**Request:**
```
GET /api/delay?delay_value=1
```

**Response:**
```json
{
    "time_taken": 5.35
}
```

## Testing with Postman

Import `postman_collection.json` into Postman for pre-configured requests.

## Project Structure

```
├── app/
│   ├── __init__.py      # Flask app factory
│   ├── config.py        # Configuration
│   ├── db.py            # Database initialization
│   ├── models.py        # Data models
│   ├── producer.py      # POST /api/items endpoint
│   └── delay_api.py     # GET /api/delay endpoint
├── worker/
│   ├── __init__.py
│   └── consumer.py      # Celery task for processing items
├── celery_worker.py     # Celery worker entry point
├── run.py               # Flask app entry point
├── requirements.txt
├── README.md
└── postman_collection.json
```

## Database Schema

The `items` table:
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- status: VARCHAR(20) NOT NULL
- item: VARCHAR(20) NOT NULL

## Architecture

1. POST /api/items → Insert row (status=pending) → Send to RabbitMQ → Return 202
2. Celery worker consumes from RabbitMQ → Update status to 'completed'
3. GET /api/delay → 5 concurrent requests via threading → Return time_taken