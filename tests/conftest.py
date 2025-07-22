import pytest
from src.scheduler import Scheduler
from unittest.mock import Mock, patch

from tests.constants import (
    test_mock_url,
    test_real_api_url,
    mock_data,
)


@pytest.fixture
def mock_api_response():
    return mock_data


@pytest.fixture
def scheduler(mock_api_response):
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        return Scheduler(test_mock_url)


@pytest.fixture
def scheduler_with_real_api():
    return Scheduler(test_real_api_url)
