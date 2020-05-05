from rest_framework import serializers

from apps.events.models import Event


class DetailEventSerializer(serializers.ModelSerializer):
    # Returns True if logged in user participates in current event
    has_participation = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'title', 'date_start', 'participants_count', 'has_participation', 'description', 'owner_name')
        read_only_fields = ('id', 'owner_name', 'participants_count', 'has_participation')
        model = Event

    def get_has_participation(self, event):
        if not self.context['request'].user.is_anonymous:
            return event.has_participation(self.context['request'].user)

        return False
