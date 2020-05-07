from django.urls import path, include
from .views import sign_in, sign_up, logout, check_session

urlpatterns = [
    path('sign_in/', sign_in),
    path('sign_up/', sign_up),
    path('logout/', logout),
    path('check_session/', check_session),
]
