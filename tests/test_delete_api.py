import pytest
import requests
import json
from tests.base_test import BaseTest
from config.config import Config
from tests.test_post_api import create_macbook

class TestDeleteAPI(BaseTest):
    """Test class for DELETE API endpoints"""
    
    def test_delete_macbook(self, create_macbook):
        """Test deleting an existing MacBook object via DELETE request"""
        created_id = create_macbook["id"]
        
        print(f"\nDeleting object with ID: {created_id}")
        print("Original object data:")
        print(json.dumps(create_macbook, indent=2))
        
        # Make the DELETE request
        response = requests.delete(
            f"{Config.BASE_URL}/objects/{created_id}",
            headers={"Content-Type": "application/json"}
        )
        
        # Assert status code is 200
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        
        # Get the response data
        response_data = response.json()
        
        # Assert the response indicates successful deletion
        assert "message" in response_data, "Response should contain a message"
        print(f"\nServer response: {response_data['message']}")
        
        # Verify the object was actually deleted by attempting to GET it
        get_response = requests.get(f"{Config.BASE_URL}/objects/{created_id}")
        assert get_response.status_code == 404, "Object should not exist after deletion"
        
        # Print verification of deletion
        print(f"\nVerified: Object with ID {created_id} no longer exists (404 Not Found)")
        
    def test_delete_nonexistent_object(self):
        """Test deleting a non-existent object returns appropriate error"""
        non_existent_id = "nonexistent123"
        
        # Make the DELETE request
        response = requests.delete(
            f"{Config.BASE_URL}/objects/{non_existent_id}",
            headers={"Content-Type": "application/json"}
        )
        
        # Assert status code is 404
        assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}"
        
        # Print verification
        print(f"\nVerified: Cannot delete non-existent object (404 Not Found)") 