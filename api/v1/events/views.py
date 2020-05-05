from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from apps.events.models import Event
from apps.events.services import participate_event, withdraw_from_event
from .permissions import AllowOwnerEditEvent
from .serializers import DetailEventSerializer


class EventsViewSet(ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, AllowOwnerEditEvent)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']
    serializer_class = DetailEventSerializer

    def get_queryset(self):
        return (
            Event.objects
            .select_related('owner')
            .prefetch_user_participation(self.request.user)
        )

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @swagger_auto_schema(methods=['post'], request_body=no_body)
    @action(detail=True, methods=['post'])
    def participate(self, request, *args, **kwargs):
        """
        Mark user as participant of event
        """
        event = self.get_object()
        participate_event(self.request.user, event)
        return Response(status=HTTP_204_NO_CONTENT)

    @swagger_auto_schema(methods=['post'], request_body=no_body)
    @action(detail=True, methods=['post'])
    def withdraw(self, request, *args, **kwargs):
        """
        Withdraw event participation
        """
        event = self.get_object()
        withdraw_from_event(self.request.user, event)
        return Response(status=HTTP_204_NO_CONTENT)
