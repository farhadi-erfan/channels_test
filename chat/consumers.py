import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer

from chat.models import User
from chat.serializers import NotificationSerializer


# class ChatConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         self.accept()
#         self.user = self.scope['user']
#
#         if self.user.is_staff:
#             async_to_sync(self.channel_layer.group_add)(
#                 'admins',
#                 self.channel_name
#             )
#             async_to_sync(self.channel_layer.group_add)(
#                 'room',
#                 self.channel_name
#             )
#         else:
#             Notification.objects.filter(verb=f'request_to_add {self.user.username}').mark_all_as_deleted()
#             notify.send(self.user, recipient=User.objects.filter(is_staff=True), verb=f'request_to_add {self.user.username}',
#                         description=self.channel_name)
#             async_to_sync(self.channel_layer.group_add)(
#                 'admins',
#                 self.channel_name
#             )
#             async_to_sync(self.channel_layer.group_send)(
#                 'admins',
#                 {'type': 'new_notification'}
#             )
#             async_to_sync(self.channel_layer.group_discard)(
#                 'admins',
#                 self.channel_name
#             )
#
#         self.send_json({'message': 'you have been connected'})
#
#     def disconnect(self, close_code):
#         # Leave room group
#         if self.user.is_staff:
#             async_to_sync(self.channel_layer.group_discard)(
#                 'admins',
#                 self.channel_name
#             )
#         async_to_sync(self.channel_layer.group_discard)(
#             'room',
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     def receive_json(self, content, **kwargs):
#         if content['type'] == 'admit':
#             channel_name = content['channel_name']
#             async_to_sync(self.channel_layer.group_add)(
#                 'room',
#                 channel_name
#             )
#             Notification.objects.filter(verb='request_to_add', description=channel_name).mark_all_as_read(
#                 recipient=self.user)
#         elif content['type'] == 'chat':
#             message = content['message']
#
#             # Send message to room group
#             async_to_sync(self.channel_layer.group_send)(
#                 'room',
#                 {
#                     'type': 'chat_message',
#                     'message': message
#                 }
#             )
#
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send_json(content={'message': message})
#
#     def new_notification(self, event):
#         if self.user.is_staff:
#             self.send_json(NotificationSerializer(self.user.notifications.filter(verb__startswith='request_to_add').unread(),
#                                                   many=True).data)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': f'you just said: {message}'
        }))