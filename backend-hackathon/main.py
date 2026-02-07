"""
FastAPI main application for Sign Language Interpreter Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import time

# Import routers
from routers import stt, tts, sign_output, session_log, dialogue, config
from models.schemas import HealthResponse

# Load environment variables
load_dotenv()

# Track server start time
start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    print("🚀 Starting Sign Language Interpreter API...")
    print(f"📍 Environment: {os.getenv('DEBUG', 'False')}")
    
    yield
    
    # Shutdown
    print("👋 Shutting down Sign Language Interpreter API...")
    
    # Cleanup services
    from services.coqui_tts import get_coqui_service
    from services.signall_sdk import get_signall_service
    
    coqui_service = get_coqui_service()
    await coqui_service.close()
    
    signall_service = get_signall_service()
    await signall_service.close()


# Create FastAPI app
app = FastAPI(
    title="Sign Language Interpreter API",
    description="Backend API for Sign Language Interpreter mobile app with ML-powered endpoints",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS - Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stt.router)
app.include_router(tts.router)
app.include_router(sign_output.router)
app.include_router(session_log.router)
app.include_router(dialogue.router)
app.include_router(config.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Sign Language Interpreter API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    uptime_seconds = int(time.time() - start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    
    uptime_str = f"{hours}h {minutes}m"
    
    return HealthResponse(
        status="ok",
        uptime=uptime_str,
        version="1.0.0"
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )
