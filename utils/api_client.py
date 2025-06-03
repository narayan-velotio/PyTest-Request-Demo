import requests
from typing import Optional, Dict, Any
from config.config import Config

class APIClient:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update(Config.get_headers())

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Send GET request to the specified endpoint"""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, params=params, timeout=self.timeout)

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Send POST request to the specified endpoint"""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=json, data=data, timeout=self.timeout)

    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Send PUT request to the specified endpoint"""
        url = f"{self.base_url}{endpoint}"
        return self.session.put(url, json=json, timeout=self.timeout)

    def delete(self, endpoint: str) -> requests.Response:
        """Send DELETE request to the specified endpoint"""
        url = f"{self.base_url}{endpoint}"
        return self.session.delete(url, timeout=self.timeout)

    def patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Send PATCH request to the specified endpoint"""
        url = f"{self.base_url}{endpoint}"
        return self.session.patch(url, json=json, timeout=self.timeout) 