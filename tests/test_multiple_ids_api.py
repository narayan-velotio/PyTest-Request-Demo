import pytest
from tests.base_test import BaseTest

class TestMultipleObjectsAPI(BaseTest):
    def test_get_multiple_objects_by_ids(self, product_schema):
        """Test getting multiple objects using id parameters"""
        # IDs to query
        ids = ["3", "5", "10"]
        
        # Construct query parameters
        query_params = [("id", id_) for id_ in ids]
        
        # Send GET request with multiple id parameters
        response = self.api_client.get(self.base_endpoint, params=query_params)
        
        # Validate response
        self.assert_status_code(response, 200)
        objects = response.json()
        
        # Basic validations
        assert isinstance(objects, list), "Response should be a list of objects"
        assert len(objects) == len(ids), f"Expected {len(ids)} objects, got {len(objects)}"
        
        # Validate each object's schema
        for obj in objects:
            mock_response = type('Response', (), {'json': lambda self: obj})()
            self.validate_response_schema(mock_response, product_schema)
        
        # Validate specific objects
        expected_objects = {
            "3": {
                "name": "Apple iPhone 12 Pro Max",
                "data": {
                    "color": "Cloudy White",
                    "capacity GB": 512
                }
            },
            "5": {
                "name": "Samsung Galaxy Z Fold2",
                "data": {
                    "price": 689.99,
                    "color": "Brown"
                }
            },
            "10": {
                "name": "Apple iPad Mini 5th Gen",
                "data": {
                    "Capacity": "64 GB",
                    "Screen size": 7.9
                }
            }
        }
        
        # Validate each object's specific fields
        for obj in objects:
            obj_id = obj["id"]
            expected = expected_objects[obj_id]
            
            # Validate name
            assert obj["name"] == expected["name"], f"Object {obj_id} has incorrect name"
            
            # Validate data fields
            for key, value in expected["data"].items():
                assert obj["data"][key] == value, f"Object {obj_id} has incorrect {key}"

    def test_get_multiple_objects_partial_invalid(self):
        """Test getting multiple objects with some invalid IDs"""
        # Mix of valid and invalid IDs
        ids = ["3", "999", "10", "invalid_id"]
        query_params = [("id", id_) for id_ in ids]
        
        response = self.api_client.get(self.base_endpoint, params=query_params)
        
        # Validate response
        self.assert_status_code(response, 200)
        objects = response.json()
        
        # Should only return valid objects
        assert len(objects) == 2, "Should only return valid objects"
        
        # Verify returned objects are the valid ones
        returned_ids = [obj["id"] for obj in objects]
        assert "3" in returned_ids, "Valid ID 3 should be in response"
        assert "10" in returned_ids, "Valid ID 10 should be in response"
        
    def test_get_multiple_objects_empty_ids(self):
        """Test getting objects with no IDs provided"""
        response = self.api_client.get(self.base_endpoint, params=[("id", "")])
        
        # Should return 200 with empty list or all objects
        self.assert_status_code(response, 200)
        objects = response.json()
        assert isinstance(objects, list), "Response should be a list"

    @pytest.mark.parametrize("ids,expected_names", [
        (
            ["3", "5"],
            ["Apple iPhone 12 Pro Max", "Samsung Galaxy Z Fold2"]
        ),
        (
            ["10"],
            ["Apple iPad Mini 5th Gen"]
        ),
        (
            ["3", "10"],
            ["Apple iPhone 12 Pro Max", "Apple iPad Mini 5th Gen"]
        )
    ])
    def test_get_multiple_objects_combinations(self, ids, expected_names, product_schema):
        """Test different combinations of multiple IDs"""
        query_params = [("id", id_) for id_ in ids]
        response = self.api_client.get(self.base_endpoint, params=query_params)
        
        # Validate response
        self.assert_status_code(response, 200)
        objects = response.json()
        
        # Validate number of objects
        assert len(objects) == len(ids), f"Expected {len(ids)} objects, got {len(objects)}"
        
        # Validate schema
        for obj in objects:
            mock_response = type('Response', (), {'json': lambda self: obj})()
            self.validate_response_schema(mock_response, product_schema)
        
        # Validate names
        returned_names = [obj["name"] for obj in objects]
        assert sorted(returned_names) == sorted(expected_names), "Object names don't match expected names" 