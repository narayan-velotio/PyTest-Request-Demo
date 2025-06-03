import pytest
from utils.api_client import APIClient

class BaseTest:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup method that runs before each test"""
        self.api_client = APIClient()
        self.base_endpoint = "/objects"  # Base endpoint for the objects API
        yield
        
    @pytest.fixture
    def product_schema(self):
        """Common schema for product objects"""
        return {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "data": {
                    "type": ["object", "null"],
                    "properties": {
                        "color": {"type": ["string", "null"]},
                        "capacity": {"type": ["string", "null"]},
                        "capacity GB": {"type": ["integer", "null"]},
                        "price": {"type": ["number", "null"]},
                        "generation": {"type": ["string", "null"]},
                        "year": {"type": ["integer", "null"]},
                        "CPU model": {"type": ["string", "null"]},
                        "Hard disk size": {"type": ["string", "null"]},
                        "Strap Colour": {"type": ["string", "null"]},
                        "Case Size": {"type": ["string", "null"]},
                        "Color": {"type": ["string", "null"]},
                        "Description": {"type": ["string", "null"]},
                        "Screen size": {"type": ["number", "null"]},
                        "Capacity": {"type": ["string", "null"]},
                        "Generation": {"type": ["string", "null"]},
                        "Price": {"type": ["string", "null"]}
                    },
                    "additionalProperties": True
                }
            },
            "required": ["id", "name", "data"]
        }
        
    def validate_response_schema(self, response, schema):
        """Validate response against JSON schema"""
        try:
            from jsonschema import validate
            validate(instance=response.json(), schema=schema)
            return True
        except Exception as e:
            pytest.fail(f"Response schema validation failed: {str(e)}")
            
    def assert_status_code(self, response, expected_status_code):
        """Assert response status code"""
        assert response.status_code == expected_status_code, \
            f"Expected status code {expected_status_code}, but got {response.status_code}"
            
    def assert_response_key(self, response, key):
        """Assert response contains a specific key"""
        assert key in response.json(), f"Response does not contain key: {key}"
        
    def assert_product_fields(self, product):
        """Assert product contains required fields"""
        assert "id" in product, "Product missing 'id' field"
        assert "name" in product, "Product missing 'name' field"
        assert "data" in product or product["data"] is None, "Product missing 'data' field" 