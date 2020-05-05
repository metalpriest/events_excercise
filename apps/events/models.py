from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel


User = get_user_model()


class EventQueryset(models.QuerySet):
    def prefetch_user_participation(self, user):
        queryset = User.objects.filter(pk=user.pk).only('id')

        # TODO: possible to make more efficient prefetch with explicit m:m table Participant
        return self.prefetch_related(
            models.Prefetch('participants', queryset, to_attr='participants_prefetch')
        )


class Event(TimeStampedModel):
    objects = EventQueryset.as_manager()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    date_start = models.DateTimeField(db_index=True)
    participants = models.ManyToManyField(User, related_name='participated_in')
    participants_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-date_start',)

    @property
    def owner_name(self):
        return self.owner.get_short_name()

    def has_participation(self, user) -> bool:
        """
        Returns True if given user participates in current event
        """
        if hasattr(self, 'participants_prefetch'):
            return any(user.id == user.id for user in self.participants_prefetch)

        return self.participants.filter(id=user.id).exists()
