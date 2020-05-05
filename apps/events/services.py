from django.db import IntegrityError
from django.db.models import F

from apps.accounts.models import User
from apps.events.models import Event


def participate_event(user: User, event: Event) -> bool:
    """
    Set user as participant for the given user.
    """
    if not event.participants.filter(id=user.id).exists():
        event.participants.add(user)
        recalculate_participants(event)
        return True

    return False


def withdraw_from_event(user: User, event: Event) -> bool:
    """
    Withdraw user from participation for the given event.
    """
    if event.participants.filter(id=user.id).exists():
        event.participants.remove(user)
        recalculate_participants(event, withdraw=True)

        return True

    return False


def recalculate_participants(event: Event, withdraw=False):
    """
    Recalculate participants by incrementing/decrementing one participant.
    This method is efficient but accuracy can struggle a bit due to race conditions.
    """

    try:
        Event.objects.filter(pk=event.pk).update(participants_count=F('participants_count') + (-1 if withdraw else 1))
    except IntegrityError:
        # In case if it tries to decrease to negative value
        if not withdraw:
            raise
