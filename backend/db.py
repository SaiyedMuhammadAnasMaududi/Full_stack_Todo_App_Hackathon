from sqlmodel import create_engine
from sqlalchemy.pool import StaticPool
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Configure engine based on database type
if "sqlite" in DATABASE_URL:
    # SQLite-specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False  # Set to True for debugging SQL queries
    )
else:
    # PostgreSQL-specific configuration with connection pooling
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,      # Verify connections before use (essential for Neon)
        pool_recycle=300,        # Recycle connections to prevent timeouts
        pool_timeout=30,
        echo=False  # Set to True for debugging SQL queries
    )

# Session dependency
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session

# Create a session instance for direct use
def SessionLocal():
    return Session(engine)