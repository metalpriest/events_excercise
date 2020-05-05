import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def api_client():
    yield APIClient()


@pytest.fixture()
def logged_client(user):
    client = APIClient()
    client.force_login(user)
    client.user = user
    
    yield client


@pytest.fixture()
def datetime_to_representation():
    """
    datetime -> isoformat like rest framework does
    """
    def _datetime_to_representation(value):
        value = value.isoformat()
        if value.endswith('+00:00'):
            value = value[:-6] + 'Z'

        return value

    yield _datetime_to_representation
