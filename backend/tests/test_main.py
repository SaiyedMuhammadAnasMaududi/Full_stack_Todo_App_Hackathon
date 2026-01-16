import pytest
from main import app
import models
from db import engine


def test_app_creation():
    """Test that the app is created successfully"""
    assert app is not None
    assert app.title == "Secure Multi-User Todo Backend API"


def test_models_available():
    """Test that models are available"""
    assert hasattr(models, 'User')
    assert hasattr(models, 'Task')


def test_database_engine():
    """Test that database engine is configured"""
    assert engine is not None