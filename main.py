from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables

from routes.orders import router as order_router
from routes.stats import router as stats_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_tables()
    print("Database tables created successfully.")
    yield
    print("Application shutdown complete.")
    
app = FastAPI(
    title="MealFlow Order Management API",
    description="API for managing orders in a MealFlow system.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(order_router)
app.include_router(stats_router)

@app.get("/")
def health_check():
    return {"status": "Welcome to the MealFlow Order Management API! The API is up and running."}
