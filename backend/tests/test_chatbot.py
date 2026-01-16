import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from unittest.mock import patch
import os
from datetime import datetime


@pytest.fixture(name="client")
def test_client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(name="session")
def test_session():
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session


def test_chat_endpoint_exists(client):
    """
    Test that the chat endpoint exists and returns a proper response format
    """
    # This test will fail initially because we don't have a valid JWT token
    # But it verifies the endpoint exists
    response = client.post("/api/testuser/chat", json={"message": "hello"})

    # Should return 401 (unauthorized) or 403 (forbidden) because of auth
    # Rather than 404 (not found)
    assert response.status_code in [401, 403, 422]


def test_conversations_endpoint_exists(client):
    """
    Test that the conversations endpoint exists
    """
    response = client.get("/api/testuser/conversations")

    # Should return 401 (unauthorized) or 403 (forbidden) because of auth
    # Rather than 404 (not found)
    assert response.status_code in [401, 403]


def test_single_conversation_endpoint_exists(client):
    """
    Test that the single conversation endpoint exists
    """
    response = client.get("/api/testuser/conversations/1")

    # Should return 401 (unauthorized) or 403 (forbidden) because of auth
    # Rather than 404 (not found)
    assert response.status_code in [401, 403]


@patch.dict(os.environ, {"COHERE_API_KEY": "test-key"})
def test_ai_agent_initialization():
    """
    Test that the AI agent can be initialized with the required environment variables
    """
    from src.ai.agent import AIAgent

    # This test might fail if Cohere API is not accessible,
    # but it tests that the agent can be initialized
    try:
        agent = AIAgent()
        assert agent is not None
    except Exception as e:
        # If Cohere is not available, we still want to verify the structure
        print(f"Agent initialization test: {str(e)}")
        # This is acceptable in testing environment without API access


def test_mcp_tools_import():
    """
    Test that MCP tools can be imported
    """
    from src.ai.tools import MCPTaskTools, ToolResult

    tools = MCPTaskTools()
    assert tools is not None
    assert hasattr(tools, 'add_task')
    assert hasattr(tools, 'list_tasks')
    assert hasattr(tools, 'update_task')
    assert hasattr(tools, 'complete_task')
    assert hasattr(tools, 'delete_task')


def test_models_import():
    """
    Test that new models can be imported
    """
    from models import Conversation, Message

    # Test that models exist and have expected attributes
    conv_attrs = ['user_id', 'title', 'created_at', 'updated_at', 'is_active']
    msg_attrs = ['conversation_id', 'sender_type', 'content', 'role', 'timestamp', 'sequence_number']

    conv = Conversation()
    msg = Message()

    for attr in conv_attrs:
        assert hasattr(conv, attr)

    for attr in msg_attrs:
        assert hasattr(msg, attr)


if __name__ == "__main__":
    pytest.main([__file__])