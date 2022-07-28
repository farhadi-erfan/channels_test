from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from notifications.signals import notify
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from chat.models import User
from chat.serializers import MyTokenObtainPairSerializer, UserSerializer


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


class Login(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (permissions.AllowAny,)
    my_tags = ['accounts']

    def post(self, request, *args, **kwargs):
        data = request.data

        user = get_object_or_404(User, username=data['username'])
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            notify.send(user, recipient=user, verb=f'dear {user.full_name}, you have successfully logged in')
            return Response({'user': UserSerializer().to_representation(user), **serializer.validated_data},
                            status=status.HTTP_200_OK)
