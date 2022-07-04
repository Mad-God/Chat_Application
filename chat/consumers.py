import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # for initial request that comes in from client
        self.accept()
        self.room_group_name = str(datetime.now().second)
        self.send(text_data = json.dumps({
            "type":"connection_established",
            "message":"You are now connected",
        }))
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        # breakpoint()
    
    def receive(self, text_data): # for when the client sends messages
        text_data_json = json.loads(text_data)
        # breakpoint()
        message = text_data_json["message"]
        print(message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':"chat_message",
                "message":message
            }
        )

    def chat_message(self, event):
        # breakpoint()
        message = event["message"]
        self.send(text_data=json.dumps({
            "type":"chat",
            "message":message,
        }))


    # def disconnect(): # for when the client disconnects from the client


