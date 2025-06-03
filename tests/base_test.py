import pytest
import requests
from config.config import Config
import json
from utils.api_client import APIClient

class BaseTest:
    """Base test class with common functionality"""
    
    def setup_method(self):
        """Setup method run before each test"""
        self.base_url = Config.BASE_URL
        self.base_endpoint = "/objects"  # Base endpoint for the objects API
        self.api_client = requests.Session()
        print(f"\nUsing base URL: {self.base_url}")
        print(f"Using endpoint: {self.base_endpoint}")
    
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
        
    def get_full_url(self, path=""):
        """Get full URL for a given path"""
        # Remove leading slash from path if it exists to avoid double slashes
        if path.startswith("/"):
            path = path[1:]
        return f"{self.base_url}/{path}"
    
    def validate_response_schema(self, response, schema):
        """Validate response against JSON schema"""
        try:
            from jsonschema import validate
            response_json = response.json()
            print(f"\nValidating schema for response: {json.dumps(response_json, indent=2)[:500]}")
            validate(instance=response_json, schema=schema)
        except Exception as e:
            print(f"Schema validation error: {str(e)}")
            raise
            
    def assert_status_code(self, response, expected_status_code):
        """Assert response status code"""
        print(f"\nRequest URL: {response.request.url}")
        print(f"Request Method: {response.request.method}")
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        print(f"Response Body: {response.text[:1000]}")  # First 1000 chars to avoid huge output
        
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
