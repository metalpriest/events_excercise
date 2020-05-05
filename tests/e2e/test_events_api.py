import json
from datetime import datetime
from django.utils import timezone

import pytest
from rest_framework.status import HTTP_204_NO_CONTENT

from apps.events.models import Event
from tests.factories import EventFactory


@pytest.mark.django_db
class TestEventsCrud:
    def detail_url(self, event):
        return f'/api/v1/events/{event.pk}/'

    def list_url(self):
        return '/api/v1/events/'

    def test_create_event_authorized_returns_201(self, logged_client):
        event_data = {
            'title': 'test event',
            'description': 'some interesting meeting',
            'date_start': '2020-10-10T10:15:00Z'
        }

        response = logged_client.post(self.list_url(), data=json.dumps(event_data), content_type='application/json')
        assert response.status_code == 201

        response = response.json()

        event = Event.objects.get(id=response['id'])

        assert response['title'] == event_data['title']
        assert response['description'] == event_data['description']
        assert response['date_start'] == event_data['date_start']

        assert event.title == event_data['title']
        assert event.description == event_data['description']
        assert event.owner == logged_client.user

    def test_create_event_unauthorized_returns_403(self, api_client):
        event_data = {
            'title': 'test event',
            'description': 'some interesting meeting',
            'date_start': '2020-10-10T10:15:00Z'
        }

        response = api_client.post(self.list_url(), data=json.dumps(event_data), content_type='application/json')
        assert response.status_code == 403

    @pytest.mark.parametrize('is_authorized', [True, False])
    def test_retrieve_event_returns_200(self, logged_client, api_client, datetime_to_representation, is_authorized):
        """
        Check event retrieve for authorized and anonymous users
        """
        client = logged_client if is_authorized else api_client
        event = EventFactory()

        response = client.get(self.detail_url(event), content_type='application/json')
        assert response.status_code == 200

        response = response.json()

        assert response['title'] == event.title
        assert response['owner_name'] == event.owner.email.split('@')[0]
        assert response['description'] == event.description
        assert response['date_start'] == datetime_to_representation(event.date_start)
        assert response['participants_count'] == 0

    def test_patch_event_authorized_returns_200(self, logged_client):
        event = EventFactory(owner=logged_client.user)
        event_data = {'title': "New title"}

        response = logged_client.patch(
            self.detail_url(event),
            data=json.dumps(event_data),
            content_type='application/json')

        assert response.status_code == 200
        response = response.json()

        assert response['title'] == event_data['title']

        event.refresh_from_db()
        assert event.title == event_data['title']

    def test_patch_unauthorized_returns_403(self, api_client):
        event = EventFactory()

        response = api_client.patch(
            self.detail_url(event),
            data=json.dumps({'title': "New title"}),
            content_type='application/json')

        assert response.status_code == 403

    def test_patch_others_user_event_returns_403(self, logged_client):
        # event is not related to logged-in user
        event = EventFactory()

        response = logged_client.patch(
            self.detail_url(event),
            data=json.dumps({'title': "New title"}),
            content_type='application/json')

        assert response.status_code == 403

    def test_put_event_returns_405(self, logged_client):
        """
        Put is not allowed. Patch should be used instead
        """
        event = EventFactory(owner=logged_client.user)

        response = logged_client.put(
            self.detail_url(event),
            data=json.dumps({'title': "New title"}),
            content_type='application/json')

        assert response.status_code == 405

    @pytest.mark.parametrize('is_authorized', [True, False])
    def test_list_events_returns_events_sorted_desc(self, logged_client,
                                                    api_client, is_authorized, datetime_to_representation):
        client = logged_client if is_authorized else api_client

        first = timezone.make_aware(datetime(2020, 5, 1, 11, 15))
        last = timezone.make_aware(datetime(2020, 1, 1, 10, 15))
        middle = timezone.make_aware(datetime(2020, 5, 1, 10, 15))

        for date in (first, last, middle):
            EventFactory(date_start=date)

        response = client.get(self.list_url(), content_type='application/json')
        assert response.status_code == 200

        response = response.json()

        assert response['count'] == 3

        assert response['results'][0]['date_start'] == datetime_to_representation(first)
        assert response['results'][1]['date_start'] == datetime_to_representation(middle)
        assert response['results'][2]['date_start'] == datetime_to_representation(last)


@pytest.mark.django_db
class TestEventsActions:
    def participate_url(self, event):
        return f'/api/v1/events/{event.pk}/participate/'

    def withdraw_url(self, event):
        return f'/api/v1/events/{event.pk}/withdraw/'

    def test_participate_event_returns_204(self, logged_client):
        event = EventFactory()
        response = logged_client.post(self.participate_url(event), content_type='application/json')

        assert response.status_code == HTTP_204_NO_CONTENT

        event.refresh_from_db()
        assert event.participants_count == 1
        assert event.has_participation(logged_client.user)

    def test_withdraw_event_returns_204(self, logged_client):
        event = EventFactory(participants_count=1)
        event.participants.add(logged_client.user)

        response = logged_client.post(self.withdraw_url(event), content_type='application/json')

        assert response.status_code == HTTP_204_NO_CONTENT

        event.refresh_from_db()
        assert event.participants_count == 0
        assert not event.has_participation(logged_client.user)
