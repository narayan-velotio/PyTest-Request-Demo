import pytest
from tests.base_test import BaseTest

class TestGetAPI(BaseTest):
    def test_get_all_objects(self, product_schema):
        """Test getting all objects"""
        # Send GET request
        response = self.api_client.get(self.base_endpoint)
        
        # Validate response
        self.assert_status_code(response, 200)
        objects = response.json()
        assert isinstance(objects, list), "Response should be a list of objects"
        assert len(objects) > 0, "Response should not be empty"
        
        # Validate schema for each object
        for obj in objects:
            # Create a mock response object with the current object
            mock_response = type('Response', (), {'json': lambda self: obj})()
            self.validate_response_schema(mock_response, product_schema)

    def test_get_single_object(self, product_schema):
        """Test getting a single object"""
        # Using a known object ID
        object_id = "1"  # Google Pixel 6 Pro
        response = self.api_client.get(f"{self.base_endpoint}/{object_id}")
        
        # Validate response
        self.assert_status_code(response, 200)
        self.validate_response_schema(response, product_schema)
        
        # Validate specific fields
        product = response.json()
        assert product["id"] == "1"
        assert product["name"] == "Google Pixel 6 Pro"
        assert product["data"]["color"] == "Cloudy White"
        assert product["data"]["capacity"] == "128 GB"

    def test_get_object_with_null_data(self, product_schema):
        """Test getting an object with null data field"""
        object_id = "2"  # iPhone 12 Mini with null data
        response = self.api_client.get(f"{self.base_endpoint}/{object_id}")
        
        # Validate response
        self.assert_status_code(response, 200)
        self.validate_response_schema(response, product_schema)
        
        # Validate null data
        product = response.json()
        assert product["id"] == "2"
        assert product["name"] == "Apple iPhone 12 Mini, 256GB, Blue"
        assert product["data"] is None

    @pytest.mark.parametrize("object_id,expected_name", [
        ("7", "Apple MacBook Pro 16"),
        ("8", "Apple Watch Series 8"),
        ("13", "Apple iPad Air")
    ])
    def test_get_multiple_objects(self, object_id, expected_name, product_schema):
        """Test getting multiple different objects"""
        response = self.api_client.get(f"{self.base_endpoint}/{object_id}")
        
        # Validate response
        self.assert_status_code(response, 200)
        self.validate_response_schema(response, product_schema)
        
        # Validate name
        product = response.json()
        assert product["id"] == object_id
        assert product["name"] == expected_name

    @pytest.mark.parametrize("invalid_id", ["999999", "invalid_id"])
    def test_get_nonexistent_object(self, invalid_id):
        """Test getting an object that doesn't exist"""
        response = self.api_client.get(f"{self.base_endpoint}/{invalid_id}")
        self.assert_status_code(response, 404) 