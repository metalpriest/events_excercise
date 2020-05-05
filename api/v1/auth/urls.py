from django.urls import path, include
from .views import sign_in, sign_up

urlpatterns = [
    path('sign_in/', sign_in),
    path('sign_up/', sign_up),
]
