from channels.generic.websocket import WebsocketConsumer
from notifications.models import Notification
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from chat.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=False)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = str(user.id)
        return token

    def validate(self, attrs):
        credentials = {
            'password': attrs.get('password')
        }
        username = attrs.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            credentials['username'] = user.username
            try:
                return super().validate(credentials)
            except Exception:
                raise AuthenticationFailed()
        else:
            raise AuthenticationFailed()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']
        read_only_fields = ['id']


class GenericNotificationRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, User):
            serializer = UserSerializer(value)
        elif isinstance(value, WebsocketConsumer):
            return value.channel_name
        # if isinstance(value, Bar):
        #     serializer = BarSerializer(value)

        return serializer.data


class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(User, read_only=True)
    unread = serializers.BooleanField(read_only=True)
    target = GenericNotificationRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = ['recipient', 'unread', 'target', 'verb', 'description']
