"""
Integration tests for sequence API CRUD operations.
Tests the complete workflow from API to storage.
"""

import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

from infrastructure.api.main import app


@pytest.fixture
def client():
    """Create test client with initialized services."""
    # Services are automatically initialized via lifespan
    return TestClient(app)


def test_sequence_crud_workflow(client):
    """Test complete sequence CRUD workflow."""

    # 1. Create sequence
    create_response = client.post(
        "/api/sequences", json={"name": "Test Sequence", "length": 5}
    )
    assert create_response.status_code == 200
    created_sequence = create_response.json()
    sequence_id = created_sequence["id"]

    # Verify created sequence structure
    assert created_sequence["name"] == "Test Sequence"
    assert len(created_sequence["beats"]) == 5
    assert created_sequence["id"] is not None

    # 2. Retrieve sequence by ID
    get_response = client.get(f"/api/sequences/{sequence_id}")
    assert get_response.status_code == 200
    retrieved_sequence = get_response.json()
    assert retrieved_sequence["name"] == "Test Sequence"
    assert retrieved_sequence["id"] == sequence_id

    # 3. Update sequence
    update_data = retrieved_sequence.copy()
    update_data["name"] = "Updated Test Sequence"
    update_response = client.put(f"/api/sequences/{sequence_id}", json=update_data)
    assert update_response.status_code == 200
    updated_sequence = update_response.json()
    assert updated_sequence["name"] == "Updated Test Sequence"
    assert updated_sequence["id"] == sequence_id

    # 4. Verify current sequence
    current_response = client.get("/api/sequences/current")
    assert current_response.status_code == 200
    current_sequence = current_response.json()
    assert current_sequence is not None
    assert current_sequence["id"] == sequence_id
    assert current_sequence["name"] == "Updated Test Sequence"


def test_get_nonexistent_sequence(client):
    """Test retrieving a sequence that doesn't exist."""
    response = client.get("/api/sequences/nonexistent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_nonexistent_sequence(client):
    """Test updating a sequence that doesn't exist."""
    update_data = {
        "id": "nonexistent-id",
        "name": "Test",
        "word": "",
        "beats": [],
        "start_position": None,
        "metadata": {},
    }
    response = client.put("/api/sequences/nonexistent-id", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_sequence_validation(client):
    """Test sequence creation with invalid data."""
    # Test empty name
    response = client.post("/api/sequences", json={"name": "", "length": 5})
    assert response.status_code == 400

    # Test invalid length
    response = client.post("/api/sequences", json={"name": "Test", "length": 0})
    assert response.status_code == 400


def test_current_sequence_when_none_exists(client):
    """Test getting current sequence when none exists."""
    # This test assumes a fresh state - in a real test we'd clear the repository
    response = client.get("/api/sequences/current")
    # Should return 200 with null content when no current sequence
    assert response.status_code == 200
    # The response might be null or an empty response depending on implementation


def test_multiple_sequences_current_tracking(client):
    """Test that current sequence tracking works with multiple sequences."""

    # Create first sequence
    response1 = client.post(
        "/api/sequences", json={"name": "First Sequence", "length": 3}
    )
    assert response1.status_code == 200
    first_id = response1.json()["id"]

    # Create second sequence
    response2 = client.post(
        "/api/sequences", json={"name": "Second Sequence", "length": 4}
    )
    assert response2.status_code == 200
    second_id = response2.json()["id"]

    # Current sequence should be the most recently created (second)
    current_response = client.get("/api/sequences/current")
    assert current_response.status_code == 200
    current_sequence = current_response.json()
    assert current_sequence["id"] == second_id
    assert current_sequence["name"] == "Second Sequence"

    # Verify we can still get the first sequence by ID
    get_first_response = client.get(f"/api/sequences/{first_id}")
    assert get_first_response.status_code == 200
    assert get_first_response.json()["name"] == "First Sequence"


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
