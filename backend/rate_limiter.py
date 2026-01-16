from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI
import os

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

def add_rate_limiting(app: FastAPI):
    """
    Add rate limiting to the FastAPI application
    """
    # Add the rate limiter to the app
    app.state.limiter = limiter
    app.add_exception_handler(429, _rate_limit_exceeded_handler)

    # Get rate limits from environment variables or use defaults
    task_endpoints_rate = os.getenv("TASK_ENDPOINTS_RATE_LIMIT", "100/minute")

    return limiter, task_endpoints_rate