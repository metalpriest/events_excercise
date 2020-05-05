from django.contrib.auth import login, authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from .serializers import UserSerializer


@swagger_auto_schema(methods=['post'], request_body=UserSerializer)
@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    login(request._request, user)

    return Response(serializer.data, status=HTTP_201_CREATED)


@swagger_auto_schema(methods=['post'], request_body=UserSerializer)
@api_view(['POST'])
def sign_in(request):
    if not request.data.get('username'):
        raise ValidationError({'username': ["Email is empty"]})

    if not request.data.get('password'):
        raise ValidationError({'username': ["Password is empty"]})

    user = authenticate(
        request._request,
        username=request.data['username'],
        password=request.data['password'])

    if not user:
        raise ValidationError({'username': ["Email or password didn't match"]})

    login(request._request, user)
    # TODO: user details or profile should returned
    return Response({'id': user.id, 'email': user.email}, status=HTTP_200_OK)
