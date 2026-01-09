import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request
import models
from db import engine
from routes import tasks
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Global metrics storage
class MetricsCollector:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.response_times = deque(maxlen=1000)  # Store last 1000 response times
        self.endpoint_stats = defaultdict(lambda: {"count": 0, "errors": 0, "times": deque(maxlen=100)})

    def record_request(self, endpoint: str, method: str, status_code: int, response_time: float):
        self.request_count += 1
        if 400 <= status_code < 600:
            self.error_count += 1

        self.response_times.append(response_time)

        endpoint_key = f"{method} {endpoint}"
        self.endpoint_stats[endpoint_key]["count"] += 1
        if 400 <= status_code < 600:
            self.endpoint_stats[endpoint_key]["errors"] += 1
        self.endpoint_stats[endpoint_key]["times"].append(response_time)

    def get_metrics(self):
        total_requests = self.request_count
        total_errors = self.error_count
        error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0

        # Calculate percentiles
        sorted_times = sorted(list(self.response_times))
        p50_idx = int(len(sorted_times) * 0.5) if len(sorted_times) > 0 else 0
        p95_idx = int(len(sorted_times) * 0.95) if len(sorted_times) > 0 else 0
        p99_idx = int(len(sorted_times) * 0.99) if len(sorted_times) > 0 else 0

        p50 = sorted_times[p50_idx] if p50_idx < len(sorted_times) else 0
        p95 = sorted_times[p95_idx] if p95_idx < len(sorted_times) else 0
        p99 = sorted_times[p99_idx] if p99_idx < len(sorted_times) else 0

        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0

        return {
            "total_requests": total_requests,
            "total_errors": total_errors,
            "error_rate_percent": round(error_rate, 2),
            "avg_response_time": round(avg_response_time, 4),
            "p50_response_time": round(p50, 4),
            "p95_response_time": round(p95, 4),
            "p99_response_time": round(p99, 4),
            "endpoint_stats": {
                k: {
                    "count": v["count"],
                    "errors": v["errors"],
                    "error_rate": round(v["errors"] / v["count"] * 100 if v["count"] > 0 else 0, 2),
                    "avg_time": round(sum(v["times"]) / len(v["times"]) if v["times"] else 0, 4)
                } for k, v in self.endpoint_stats.items()
            }
        }


metrics_collector = MetricsCollector()


# Initialize FastAPI app
app = FastAPI(
    title="Secure Multi-User Todo Backend API",
    description="REST API for a secure, multi-user todo application backend using Python FastAPI with JWT-based authentication and Neon Serverless PostgreSQL for data persistence. The system enforces strict user isolation for all operations.",
    version="1.0.0"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Default Next.js development server
        "http://localhost:3001",  # Alternative Next.js development server
        "https://localhost:3000",
        "https://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://127.0.0.1:3000",
        "https://127.0.0.1:3001",
        # Add your production frontend URL here
        # "https://yourdomain.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    # Additional security headers
    allow_origin_regex=r"https?://localhost(:[0-9]+)?|https?://127\.0\.0\.1(:[0-9]+)?",
)


# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"  # Or "SAMEORIGIN" if needed
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"

        return response


# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)


# Custom logging middleware with response time metrics
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    process_time = time.time() - start_time

    # Record metrics
    metrics_collector.record_request(
        endpoint=request.url.path,
        method=request.method,
        status_code=response.status_code,
        response_time=process_time
    )

    logger.info(f"Response status: {response.status_code}, Process time: {process_time:.4f}s")

    # Log slow requests
    if process_time > 0.2:  # Log requests taking more than 200ms
        logger.warning(f"Slow request: {request.method} {request.url} took {process_time:.4f}s")

    return response


from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# Include rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Include auth and task routes
from routes import auth
app.include_router(auth.router)

# Pass the limiter to the tasks router
tasks.router.limiter = limiter
app.include_router(tasks.router)


# Create database tables
@app.on_event("startup")
def on_startup():
    try:
        models.SQLModel.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")
        # Don't raise the exception to prevent app from crashing, but log it


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-backend-api"}


# Metrics endpoint
@app.get("/metrics")
def get_metrics():
    """Get application performance metrics"""
    return metrics_collector.get_metrics()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)