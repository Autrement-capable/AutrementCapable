## core/cors/config.py
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger(__name__)

def init_cors(app):
    # Log that we're initializing CORS
    logger.info("Initializing CORS middleware")
    
    origins = [
        "http://localhost:8080",
        "http://localhost:8081",
        "https://localhost:8080",
        "https://localhost:8081",
        "http://localhost:5000",
        "https://localhost:5000",
        "http://localhost:3000",
        "https://localhost:3000",
        # Add your frontend origin here
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:3000"
    ]
    
    # Log the allowed origins
    logger.info(f"CORS allowed origins: {origins}")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:[0-9]+)?",  # Allow any localhost port
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Type", "Content-Disposition"],
        max_age=600,  # Cache preflight requests for 10 minutes
    )
    
    # Add a middleware for debugging CORS issues
    @app.middleware("http")
    async def debug_cors(request, call_next):
        logger.debug(f"Incoming request: {request.method} {request.url}")
        logger.debug(f"Headers: {request.headers}")
        
        # Process the request
        response = await call_next(request)
        
        # Log the response status
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        
        return response
    
    logger.info("CORS middleware initialized")
