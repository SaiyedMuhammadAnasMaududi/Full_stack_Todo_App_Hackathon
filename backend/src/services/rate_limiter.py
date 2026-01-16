from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request, Depends
from typing import Optional
import time


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


def get_rate_limiter():
    """Get the rate limiter instance"""
    return limiter


def add_rate_limiting(app: FastAPI):
    """Add rate limiting to the FastAPI app"""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def chat_endpoint_rate_limit():
    """
    Rate limit decorator for chat endpoints
    Limits to 100 requests per hour per IP address
    """
    return limiter.limit("100/hour")


def conversation_management_rate_limit():
    """
    Rate limit decorator for conversation management endpoints
    Limits to 200 requests per hour per IP address
    """
    return limiter.limit("200/hour")


def user_specific_rate_limit(user_id: str):
    """
    Create a rate limit based on user ID
    Limits to 50 requests per hour per user
    """
    def limit_func(request: Request):
        # This would require custom logic to get user_id from request
        # For now, we'll use the existing limiter but this could be extended
        pass

    # We'll use a default limit of 50 per hour for user-specific endpoints
    return limiter.limit("50/hour")