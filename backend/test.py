"""Test suite for Medical Multi-Agents backend"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.api import app


# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_status(self):
        """Test GET /health returns success"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "ok"
    
    def test_health_has_python_version(self):
        """Test /health returns Python version"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "python" in data
        assert "3.11" in data["python"]
    
    def test_health_has_platform(self):
        """Test /health returns platform info"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "platform" in data


class TestHomeEndpoint:
    """Test home endpoint"""
    
    def test_home_message(self):
        """Test GET / returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Medical Multi Agent API" in data["message"]


class TestAPIStructure:
    """Test basic API structure"""
    
    def test_api_responds(self):
        """Test that API responds to requests"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_api_returns_json(self):
        """Test that API returns JSON responses"""
        response = client.get("/health")
        assert response.headers["content-type"].startswith("application/json")
    
    def test_404_on_missing_endpoint(self):
        """Test 404 for undefined endpoints"""
        response = client.get("/nonexistent")
        assert response.status_code == 404


def run_tests():
    """Run all tests with pytest"""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()
