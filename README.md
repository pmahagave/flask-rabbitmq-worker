

# Flask RabbitMQ Simple Worker

A simple task processing system using Flask, RabbitMQ, and SQLite with asynchronous worker.

---

## Features

- Producer API - Add items via POST `/api/items`
- **Consumer (Simple Worker)** - Process messages from RabbitMQ in background
- **Status API** - Check all items via GET `/api/items`
- **Concurrent Requests** - 5 concurrent requests via GET `/api/delay`
- **SQLite Database** - Store items with pending/completed status
- **Standalone Consumer** - Accepts raw JSON payload (NodeJS compatible)

---

##  Technologies

| Technology | Purpose |
|------------|---------|
| Flask | API endpoints |
| RabbitMQ | Message queue / Broker |
| SQLite | Database |
| Python Threading | Concurrent requests |
| pika | RabbitMQ client |

---

##  Prerequisites

- Python 3.8+
- RabbitMQ Server 4.3.2
- Erlang/OTP 26.2
- VS Code (Recommended)

---

##  Installation

### 1. Clone Repository
```bash
git clone https://github.com/pmahagave/flask-rabbitmq-worker.git
cd flask-rabbitmq-worker
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

##  RabbitMQ Setup

### Start RabbitMQ (Admin PowerShell)
```bash
cd "C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.2\sbin"
.\rabbitmq-server.bat
```

> **Keep this window open!** RabbitMQ will run in foreground.

### Check RabbitMQ Status
```bash
cd "C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.2\sbin"
.\rabbitmqctl.bat status
```

---

##  Run the Project

### Terminal 1: RabbitMQ (Admin PowerShell)
```bash
cd "C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.2\sbin"
.\rabbitmq-server.bat
```
> **Keep this window open!**

### Terminal 2: Simple Worker (VS Code)
```bash
cd C:\Users\pratiksha mahagawe\OneDrive\Desktop\Task-Submit
venv\Scripts\activate
python simple_worker.py
```

**Expected Output:**
```
 Starting Simple Worker...
 Waiting for messages... (Press CTRL+C to stop)
```

### Terminal 3: Flask Server (VS Code - New Terminal)
```bash
cd C:\Users\pratiksha mahagawe\OneDrive\Desktop\Task-Submit
venv\Scripts\activate
python run.py
```

**Expected Output:**
```
 Flask server starting on http://localhost:5000
 Available endpoints:
   POST   /api/items
   GET    /api/items
   GET    /api/delay
```

---

##  API Testing (Postman)

### 1. POST /api/items (Create Item)

**Request:**
```
Method: POST
URL: http://localhost:5000/api/items
Headers: Content-Type: application/json
Body: {"item": "book"}
```

**Response:**
```json
{
    "message": "Item received and queued",
    "item": "book",
    "status": "pending"
}
```
**Status:** `202 ACCEPTED`

**Worker Output:**
```
 Received: book
 Item 'book' marked as completed
```

---

### 2. GET /api/items (Check Status)

**Request:**
```
Method: GET
URL: http://localhost:5000/api/items
```

**Response:**
```json
{
    "items": [
        [
            1,
            "completed",
            "book"
        ]
    ]
}
```
**Status:** `200 OK`

---

### 3. GET /api/delay (Concurrent Requests)

**Request:**
```
Method: GET
URL: http://localhost:5000/api/delay?delay_value=2
```

**Response:**
```json
{
    "time_taken": 2.15,
    "requests_made": 5,
    "all_successful": true,
    "delay_value": 2
}
```
**Status:** `200 OK`

---

##  Database Schema

### Table: `items`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto increment (Primary Key) |
| status | VARCHAR(20) | pending / completed |
| item | VARCHAR(20) | book, pen, etc |

### Sample Data:
```
┌────┬──────────┬────────────┐
│ id │ status   │ item       │
├────┼──────────┼────────────┤
│ 1  │ completed│ book       │
│ 2  │ completed│ pen        │
└────┴──────────┴────────────┘
```

---

## Project Structure

```
Task-Submit/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration
│   ├── db.py              # Database
│   ├── delay_api.py       # Concurrent API
│   ├── models.py          # Database Models
│   └── producer.py        # Producer API (POST + GET)
├── worker/
│   ├── __init__.py
│   └── consumer.py        # Celery Consumer
├── simple_worker.py       # Simple Worker (Consumer)
├── run.py                 # Flask Entry Point
├── requirements.txt       # Dependencies
├── postman_collection.json # Postman Collection
├── README.md              # Documentation
└── items.db               # SQLite Database
```

---

##  Dependencies

```
Flask==2.3.3
celery==5.3.6
pika==1.3.2
requests==2.31.0
```

---

## 🔧 Troubleshooting

### RabbitMQ Connection Error
```bash
# Check if RabbitMQ is running
cd "C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.2\sbin"
.\rabbitmqctl.bat status

# Start RabbitMQ
.\rabbitmq-service.bat start
```

### Port 5000 Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Worker Not Receiving Messages
```bash
# Check RabbitMQ queues
cd "C:\Program Files\RabbitMQ Server\rabbitmq_server-4.3.2\sbin"
.\rabbitmqctl.bat list_queues
```

---


---

##  Complete Flow

```
1. POST /api/items {"item": "book"}
   ↓
2. Flask → DB insert (status: pending)
   ↓
3. Flask → RabbitMQ send
   ↓
4. Worker → Consume message
   ↓
5. Worker → DB update (status: completed)
   ↓
6. GET /api/items → {"items": [[1, "completed", "book"]]}
```


---

##  GitHub Repository

[https://github.com/pmahagave/flask-rabbitmq-worker](https://github.com/pmahagave/flask-rabbitmq-worker)



