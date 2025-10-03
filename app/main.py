"""
FastAPI Task Manager Application
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A modern task management API built with FastAPI",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware - allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Task Manager API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
