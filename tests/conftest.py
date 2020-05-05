import pytest

from .factories import EventFactory, UserFactory


@pytest.fixture()
def event():
    yield EventFactory()


@pytest.fixture()
def user():
    yield UserFactory()
