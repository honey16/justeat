from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
import os

from app.routers import auth, restaurants, customer, owner
from app.exceptions import (
    AppException, 
    app_exception_handler, 
    general_exception_handler,
    validation_exception_handler
)
from app.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

frontend_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "").split(",")
    if origin.strip()
]

app = FastAPI(
    title="Restaurant Management API",
    description="Complete API for restaurant management system with customer and owner functionality",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
        "https://justeat-iy6k.onrender.com",
        *frontend_origins,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(restaurants.router, prefix="/api")
app.include_router(customer.router, prefix="/api")
app.include_router(owner.router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to Restaurant Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "restaurant-api"}

@app.on_event("startup")
async def startup_event():
    """Log startup event"""
    logger.info("="*50)
    logger.info("Restaurant Management API starting...")
    logger.info("="*50)

@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown event"""
    logger.info("Restaurant Management API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
