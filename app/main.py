from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import connect_to_mongo, close_mongo_connection
from .routes import analytics, admin
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 Starting up application...")
    await connect_to_mongo()
    yield
    # Shutdown
    print("🛑 Shutting down application...")
    await close_mongo_connection()


# Create FastAPI application
app = FastAPI(
    title="Portfolio Backend API",
    description="Production-ready backend for personal portfolio website",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(analytics.router)
app.include_router(admin.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Portfolio Backend API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
