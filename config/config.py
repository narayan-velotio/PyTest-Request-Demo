import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Base URLs for different environments
    BASE_URL = os.getenv('BASE_URL', 'https://api.example.com')
    print(f"Using BASE_URL: {BASE_URL}")  # This will show which URL is actually being used
    
    # API Timeouts
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    
    # Authentication
    API_KEY = os.getenv('API_KEY')
    AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'test')
    
    @staticmethod
    def get_headers():
        """Return default headers for API requests"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {Config.AUTH_TOKEN}' if Config.AUTH_TOKEN else None,
            'X-API-Key': Config.API_KEY if Config.API_KEY else None
        } 