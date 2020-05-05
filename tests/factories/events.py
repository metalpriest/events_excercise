import factory
from factory import fuzzy
from django.utils import timezone

from .accounts import UserFactory
from apps.events.models import Event


class EventFactory(factory.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    description = fuzzy.FuzzyText(length=512)
    title = fuzzy.FuzzyText(length=100)
    date_start = fuzzy.FuzzyDateTime(start_dt=timezone.now())

    class Meta:
        model = Event
