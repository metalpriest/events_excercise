import pytest
from apps.events.services import participate_event, withdraw_from_event, recalculate_participants
from ..factories import UserFactory


@pytest.mark.django_db
def test_participate_event(event, user):
    participate_event(user, event)

    assert event.has_participation(user)

    other_user = UserFactory()

    assert not event.has_participation(other_user)


@pytest.mark.django_db
def test_reapply_participate_event_is_idempotent(event, user):
    """
    Ensure that reapplying participate_event with the same parameters doesn't affect participants counter
    """
    participate_event(user, event)
    participate_event(user, event)

    event.refresh_from_db()

    assert event.participants_count == 1


@pytest.mark.django_db
def test_withdraw_from_event(event, user):
    event.participants.add(user)
    event.participants_count = 1
    event.save()

    withdraw_from_event(user, event)

    assert not event.has_participation(user)

    event.refresh_from_db()

    assert event.participants_count == 0


@pytest.mark.django_db
def test_reply_withdraw_from_event_is_idempotent(event, user):
    """
    Ensure that reapplying withdraw_from_event with the same parameters doesn't affect participants counter
    """
    event.participants.add(user)
    event.participants_count = 1
    event.save()

    result = withdraw_from_event(user, event)

    assert result
    result = withdraw_from_event(user, event)
    assert not result

    event.refresh_from_db()

    assert event.participants_count == 0


@pytest.mark.django_db
def test_incr_recalculate_participants(event):
    assert event.participants_count == 0

    recalculate_participants(event)
    recalculate_participants(event)

    event.refresh_from_db()

    assert event.participants_count == 2


@pytest.mark.django_db
def test_decr_recalculate_participants(event):
    event.participants_count = 2
    event.save()

    recalculate_participants(event, withdraw=True)
    recalculate_participants(event, withdraw=True)

    event.refresh_from_db()

    assert event.participants_count == 0


@pytest.mark.django_db
def test_decr_recalculate_participants_doesnt_set_negative_value(event, transactional_db):
    assert event.participants_count == 0

    recalculate_participants(event, withdraw=True)
    event.refresh_from_db()

    assert event.participants_count == 0
