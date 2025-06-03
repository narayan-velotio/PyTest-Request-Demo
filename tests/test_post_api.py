import pytest
import requests
import json
from tests.base_test import BaseTest
from config.config import Config

@pytest.fixture
def create_macbook():
    """Fixture to create a MacBook object and return its data"""
    # Prepare the payload
    payload = {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB"
        }
    }
    
    # Make the POST request
    response = requests.post(
        f"{Config.BASE_URL}/objects",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    # Assert status code is 200
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    
    # Get the response data
    response_data = response.json()
    
    # Print the created object ID for reference
    print(f"\nCreated object with ID: {response_data['id']}")
    
    return response_data

class TestPostAPI(BaseTest):
    """Test class for POST API endpoints"""
    
    def test_create_macbook(self, create_macbook):
        """Test creating a new MacBook object via POST request"""
        response_data = create_macbook
        
        # Prepare the expected payload
        expected_payload = {
            "name": "Apple MacBook Pro 16",
            "data": {
                "year": 2019,
                "price": 1849.99,
                "CPU model": "Intel Core i9",
                "Hard disk size": "1 TB"
            }
        }
        
        # Assert the response contains the correct data
        assert response_data["name"] == expected_payload["name"], "Name in response doesn't match the request"
        assert response_data["data"] == expected_payload["data"], "Data in response doesn't match the request"
        
        # Assert that an ID was assigned
        assert "id" in response_data, "Response doesn't contain an ID"
        assert response_data["id"] is not None, "ID should not be None"
        
        # Verify the object was created by making a GET request
        get_response = requests.get(f"{Config.BASE_URL}/objects/{response_data['id']}")
        assert get_response.status_code == 200, "Failed to retrieve the created object"
        get_data = get_response.json()
        
        # Compare relevant fields
        assert get_data["id"] == response_data["id"], "ID doesn't match"
        assert get_data["name"] == response_data["name"], "Name doesn't match"
        assert get_data["data"] == response_data["data"], "Data doesn't match" 