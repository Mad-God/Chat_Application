import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from datetime import datetime


from .models import ChatGroup, TextMessage
from base.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # for initial request that comes in from client
        self.accept()
        self.room_group_name = self.scope["path"].split("/")[-1]
        self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "message": "You are now connected",
                }
            )
        )
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data):  # for when the client sends messages
        text_data_json = json.loads(text_data)
        # breakpoint()
        message = text_data_json["message"]
        sender = self.save_message(text_data_json)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username if sender else "Anonymous",
            },
        )

    def save_message(self, message):
        # breakpoint()
        if message["sender"]:
            sender = User.objects.get(id=int(message["sender"]))
            TextMessage.objects.create(
                text=message["message"],
                sender=sender,
                group=ChatGroup.objects.get(slug=self.room_group_name),
            )
        else:
            TextMessage.objects.create(
                text=message["message"],
                group=ChatGroup.objects.get(slug=self.room_group_name),
            )
            sender = None
        return sender

    def chat_message(self, event):
        message = event["message"]
        self.send(
            text_data=json.dumps(
                {"type": "chat", "message": message, "sender": event["sender"]}
            )
        )
