import pytest


@pytest.mark.django_db
def test_user_has_participation(event, user):
    assert not event.has_participation(user)
    event.participants.add(user)

    assert event.has_participation(user)
