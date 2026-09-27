# MealFlow Order Management API

A FastAPI service for managing meal delivery orders and viewing daily order summaries.

## Project Structure

```text
.
├── main.py              # FastAPI application and router registration
├── database.py          # SQLite engine, sessions, and table creation
├── models.py            # SQLModel models and request/response schemas
├── requirements.txt     # Python dependencies
└── routes/
  ├── orders.py        # Order creation, listing, lookup, and updates
  └── stats.py         # Daily order summaries
```

## Requirements

- Python 3.10+
- pip

## Setup

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the API

```powershell
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

Interactive documentation is available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

The SQLite database `MealFlow.db` is created automatically when the application starts.

## Order Statuses

Orders use one of these statuses:

- `preparing`
- `picked_up`
- `in_transit`
- `delivered`

## Endpoints

### Health check

```http
GET /
```

### Create an order

```http
POST /orders/
Content-Type: application/json
```

Example request body:

```json
{
  "customer_name": "Falak",
  "delivery_address": "Kolkata",
  "items": "Dosa"
}
```

### List orders

```http
GET /orders/
```

Optional query parameters include `status`, `created_date`, `skip`, and `limit`:

```text
GET /orders/?status=preparing&created_date=2026-09-27&skip=0&limit=20
```

### Get one order

```http
GET /orders/{order_id}
```

Returns `404` if the order does not exist.

### Update an order

```http
PATCH /orders/{order_id}
Content-Type: application/json
```

Example request body:

```json
{
  "status": "picked_up",
  "delivery_address": "Howrah"
}
```

Both fields are optional. The response records the old status, new status, and update time.

### Get a daily summary

```http
GET /stats/daily
```

Use `summary_date` to request a specific date:

```http
GET /stats/daily?summary_date=2026-09-27
```

The response includes the total order count and counts grouped by status.

Example response:

```json
{
  "date": "2026-09-27",
  "total_orders": 2,
  "by_status": {
    "preparing": 1,
    "picked_up": 1,
    "in_transit": 0,
    "delivered": 0
  }
}
```

## Development Notes

- Timestamps are stored as timezone-aware UTC datetimes.
- Tables are created on application startup.
- For request and response schemas, use the interactive Swagger documentation at `/docs`.
- To stop the development server, press `Ctrl+C` in the terminal running Uvicorn.
