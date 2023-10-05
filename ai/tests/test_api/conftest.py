import pytest

""" conftest for api tests"""


@pytest.fixture
def mock_timeslots():
    """Generate mock timeslots"""

    return [
        {"conversation_code": "A2365", "probability": 0.23, "is_frequent": True},
        {"conversation_code": "B1234", "probability": 0.23, "is_frequent": False},
    ]
