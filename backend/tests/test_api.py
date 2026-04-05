"""
Test suite for EdgeAGI backend API.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from api.database import get_db, Base
from models.database import Node, Task

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_edgeagi.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """Create test client with test database."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Override dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


class TestNodes:
    """Test node registration and management."""
    
    def test_register_node(self, client):
        """Test node registration."""
        response = client.post(
            "/api/nodes/register",
            json={
                "name": "TestNode-1",
                "cpu_cores": 4,
                "memory_total": 8.0,
                "gpu_enabled": False
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "TestNode-1"
        assert data["cpu_cores"] == 4
        assert data["status"] == "online"
        assert "id" in data
    
    def test_list_nodes(self, client):
        """Test listing nodes."""
        # First register a node
        client.post(
            "/api/nodes/register",
            json={"name": "TestNode-2", "cpu_cores": 2, "memory_total": 4.0}
        )
        
        response = client.get("/api/nodes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
    
    def test_heartbeat(self, client):
        """Test sending heartbeat."""
        # Register node first
        reg_response = client.post(
            "/api/nodes/register",
            json={"name": "TestNode-3", "cpu_cores": 2, "memory_total": 4.0}
        )
        node_id = reg_response.json()["id"]
        
        # Send heartbeat
        response = client.post(
            f"/api/nodes/{node_id}/heartbeat",
            json={"cpu_available": 2, "memory_available": 3.5, "status": "online"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["cpu_available"] == 2
        assert data["memory_available"] == 3.5


class TestTasks:
    """Test task creation and management."""
    
    def test_create_task(self, client):
        """Test creating a new task."""
        response = client.post(
            "/api/tasks",
            json={
                "type": "text_classification",
                "input_data": {"text": "Hello world"},
                "priority": 5,
                "credits_reward": 15
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "text_classification"
        assert data["status"] in ["pending", "running"]
        assert "id" in data
    
    def test_list_tasks(self, client):
        """Test listing tasks."""
        # Create a task first
        client.post(
            "/api/tasks",
            json={"type": "mock_inference", "input_data": {}, "priority": 0}
        )
        
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
    
    def test_get_task(self, client):
        """Test getting a specific task."""
        # Create task
        create_response = client.post(
            "/api/tasks",
            json={"type": "mock_inference", "input_data": {}}
        )
        task_id = create_response.json()["id"]
        
        # Get task
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
    
    def test_submit_task_result(self, client):
        """Test submitting task result."""
        # Create and get task
        create_response = client.post(
            "/api/tasks",
            json={"type": "mock_inference", "input_data": {}}
        )
        task_id = create_response.json()["id"]
        
        # Submit result
        response = client.post(
            f"/api/tasks/{task_id}/result",
            json={"result": {"output": "test_result"}}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["result"]["output"] == "test_result"


class TestCredits:
    """Test credit/reward system."""
    
    def test_get_credits(self, client):
        """Test getting credit balance."""
        # Register node (automatically gets signup bonus)
        reg_response = client.post(
            "/api/nodes/register",
            json={"name": "CreditTestNode", "cpu_cores": 2, "memory_total": 4.0}
        )
        node_id = reg_response.json()["id"]
        
        # Get credits
        response = client.get(f"/api/credits/{node_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["node_id"] == node_id
        assert data["total_balance"] >= 100  # Signup bonus


class TestSystem:
    """Test system endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_api_health(self, client):
        """Test API health endpoint."""
        response = client.get("/api/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_resources(self, client):
        """Test getting system resources."""
        response = client.get("/api/resources")
        assert response.status_code == 200
        data = response.json()
        assert "cpu_cores" in data
        assert "memory_total" in data


class TestLocalInference:
    """Test local AI inference."""
    
    def test_execute_local_sentiment(self, client):
        """Test local sentiment analysis."""
        response = client.post(
            "/api/tasks/execute_local",
            json={
                "type": "sentiment_analysis",
                "input_data": {"text": "This is great!"},
                "credits_reward": 10
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "sentiment" in data["result"]
    
    def test_execute_local_mock(self, client):
        """Test local mock inference."""
        response = client.post(
            "/api/tasks/execute_local",
            json={
                "type": "mock_inference",
                "input_data": {"test": "data"},
                "credits_reward": 5
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
