import json
import pytest
from django.contrib.auth import get_user_model

from ..factories import UserFactory

SIGN_UP_URL = '/api/v1/auth/sign_up/'
SIGN_IN_URL = '/api/v1/auth/sign_in/'

User = get_user_model()


@pytest.mark.django_db
def test_sign_up(api_client):
    response = api_client.post(
        SIGN_UP_URL,
        data=json.dumps({'username': 'foo@bar.com', 'password': 'qwerty'}),
        content_type='application/json')

    assert response.status_code == 201

    # TODO: for this exercise I use default session auth backend
    # But it can be simply changed to stateless JWT for example
    assert 'sessionid' in response.cookies

    response = response.json()

    assert User.objects.filter(id=response['id']).exists()


@pytest.mark.django_db
def test_successful_sign_in(api_client):
    user = UserFactory(username='foo@bar.com')
    user.set_password('qwerty')
    user.save()

    response = api_client.post(
        SIGN_IN_URL,
        data=json.dumps({'username': 'foo@bar.com', 'password': 'qwerty'}),
        content_type='application/json')

    assert response.status_code == 200
    assert 'sessionid' in response.cookies


@pytest.mark.django_db
def test_unsuccessful_sign_in(api_client):
    user = UserFactory(username='foo@bar.com')
    user.set_password('qwerty')
    user.save()

    response = api_client.post(
        SIGN_IN_URL,
        data=json.dumps({'username': 'foo@bar.com', 'password': 'wrong password'}),
        content_type='application/json')

    assert response.status_code == 400
    assert response.json() == {'username': ["Email or password didn't match"]}
