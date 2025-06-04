# API Test Framework

A pytest-based framework for API testing with requests library.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your configuration:
```bash
cp .env.example .env
```
Then edit the `.env` file with your actual values.

## Project Structure

```
api_test_framework/
├── config/
│   └── config.py         # Configuration management
├── utils/
│   └── api_client.py     # API client utilities
├── tests/
│   ├── base_test.py      # Base test class
│   └── test_example_api.py # Example test file
├── .env.example          # Example environment variables
├── pytest.ini           # Pytest configuration
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Running Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_example_api.py
```

Run tests in parallel:
```bash
pytest -n auto
```

Run tests with specific marker:
```bash
pytest -m smoke
```

## Test Reports

HTML reports are automatically generated after test execution and can be found in `report.html`.

### Allure Reports
The project is configured to generate Allure reports which are automatically published to GitHub Pages after each push to the main/master branch. To view the reports:

1. Run tests locally with Allure:
```bash
pytest --alluredir=allure-results
```

2. Generate and view report locally:
```bash
allure serve allure-results
```

3. View online reports:
- Go to your repository's GitHub Pages URL: `https://<username>.github.io/<repository-name>`
- The latest test report will be available there automatically after each push

## Writing Tests

1. Create a new test file in the `tests` directory
2. Import and inherit from `BaseTest` class
3. Use the provided `api_client` and assertion methods
4. Add appropriate test markers if needed

Example:
```python
from tests.base_test import BaseTest
import pytest

@pytest.mark.smoke
class TestNewAPI(BaseTest):
    def test_new_endpoint(self):
        response = self.api_client.get("/new-endpoint")
        self.assert_status_code(response, 200)
```

## Environment Variables

- `BASE_URL`: Base URL of the API
- `ENVIRONMENT`: Environment name (e.g., test, staging, prod)
- `REQUEST_TIMEOUT`: Request timeout in seconds
- `API_KEY`: API key for authentication
- `AUTH_TOKEN`: Authentication token 