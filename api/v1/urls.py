from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.events.views import EventsViewSet

router = DefaultRouter()
router.register('events', EventsViewSet, basename='event')
urlpatterns = router.urls + [
    path('auth/', include('api.v1.auth.urls'))
]
