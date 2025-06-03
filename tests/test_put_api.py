import pytest
import requests
import json
from tests.base_test import BaseTest
from config.config import Config
from tests.test_post_api import create_macbook

class TestPutAPI(BaseTest):
    """Test class for PUT API endpoints"""
    
    def test_update_macbook(self, create_macbook):
        """Test updating an existing MacBook object via PUT request"""
        created_id = create_macbook["id"]
        
        print(f"\nUpdating object with ID: {created_id}")
        
        # Prepare the updated payload
        updated_payload = {
            "name": "Apple MacBook Pro 16",
            "data": {
                "year": 2019,
                "price": 2049.99,
                "CPU model": "Intel Core i9",
                "Hard disk size": "1 TB",
                "color": "silver"
            }
        }
        
        # Make the PUT request
        response = requests.put(
            f"{Config.BASE_URL}/objects/{created_id}",
            json=updated_payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Assert status code is 200
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        
        # Get the response data
        response_data = response.json()
        
        # Assert the response contains the correct updated data
        assert response_data["name"] == updated_payload["name"], "Name in response doesn't match the request"
        assert response_data["data"] == updated_payload["data"], "Data in response doesn't match the request"
        assert response_data["id"] == created_id, "ID should not change after update"
        
        # Verify the object was updated by making a GET request
        get_response = requests.get(f"{Config.BASE_URL}/objects/{created_id}")
        assert get_response.status_code == 200, "Failed to retrieve the updated object"
        get_data = get_response.json()
        
        # Compare all fields
        assert get_data["id"] == created_id, "ID doesn't match"
        assert get_data["name"] == updated_payload["name"], "Name doesn't match"
        assert get_data["data"] == updated_payload["data"], "Data doesn't match"
        
        # Print the updated data for verification
        print("\nSuccessfully updated object with new data:")
        print(json.dumps(get_data, indent=2)) 