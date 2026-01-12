import pytest
from tests.api.client import APIClient
from tests.api.commands import CommandsAPI

# Базовый URL
@pytest.fixture
def base_url():
    return "http://localhost:8080"

@pytest.fixture
def api_client(base_url):
    return APIClient(base_url)

@pytest.fixture
def commands_api(api_client):
    return CommandsAPI(api_client)