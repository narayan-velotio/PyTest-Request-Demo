import pytest
import requests
import json
from tests.base_test import BaseTest
from config.config import Config
from tests.test_post_api import create_macbook

class TestPatchAPI(BaseTest):
    """Test class for PATCH API endpoints"""
    
    def test_partial_update_macbook(self, create_macbook):
        """Test partially updating an existing MacBook object via PATCH request"""
        created_id = create_macbook["id"]
        original_data = create_macbook["data"]  # Store original data for comparison
        
        print(f"\nPartially updating object with ID: {created_id}")
        
        # Prepare the patch payload (only updating the name)
        patch_payload = {
            "name": "Apple MacBook Pro 16 (Updated Name)"
        }
        
        # Make the PATCH request
        response = requests.patch(
            f"{Config.BASE_URL}/objects/{created_id}",
            json=patch_payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Assert status code is 200
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        
        # Get the response data
        response_data = response.json()
        
        # Assert that only the name was updated and other fields remained unchanged
        assert response_data["name"] == patch_payload["name"], "Name in response doesn't match the request"
        assert response_data["data"] == original_data, "Data object should not have changed"
        assert response_data["id"] == created_id, "ID should not change after update"
        
        # Verify the object was updated by making a GET request
        get_response = requests.get(f"{Config.BASE_URL}/objects/{created_id}")
        assert get_response.status_code == 200, "Failed to retrieve the updated object"
        get_data = get_response.json()
        
        # Compare all fields
        assert get_data["id"] == created_id, "ID doesn't match"
        assert get_data["name"] == patch_payload["name"], "Name doesn't match"
        assert get_data["data"] == original_data, "Data object should not have changed"
        
        # Print the updated data for verification
        print("\nSuccessfully updated object with new name:")
        print(json.dumps(get_data, indent=2))
        
        # Print what fields remained unchanged
        print("\nVerifying unchanged fields:")
        print("- Original price:", original_data["price"])
        print("- Original CPU model:", original_data["CPU model"])
        print("- Original Hard disk size:", original_data["Hard disk size"])
        print("- Original year:", original_data["year"]) 