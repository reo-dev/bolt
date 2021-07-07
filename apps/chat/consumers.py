# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# import json

# from apps.project.models import *

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         print('connect')
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         print('disconnect')
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         print('receive')
#         text_data_json = json.loads(text_data)

#         # x = Chat.objects.get()
#         print(text_data_json)
#         message = text_data_json['message']
#         type_ = text_data_json['type']
#         time_ = text_data_json['time']

#         # answer_id = Chat.objects.get('answer')[0].answer
#         # print('answer_id', answer_id)
#         # if message=='receive':
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'type_':type_,
#                 'time':time_,
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         print('chat')
#         message = event['message']
#         type_ = event['type_']
#         time_ = event['time']
        
#         self.send(text_data=json.dumps({
#             'message': message,
#             'type':type_,
#             'time':time_,
#         }))



from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from apps.project.models import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print('disconnect')
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print('receive')
        text_data_json = json.loads(text_data)

        # x = Chat.objects.get()
        print(text_data_json)
        message = text_data_json['message']
        type_ = text_data_json['type']
        time_ = text_data_json['time']
        bReceive = text_data_json['bReceive']
        file_ = text_data_json['file']
        chatType_ = text_data_json['chatType']

        # answer_id = Chat.objects.get('answer')[0].answer
        # print('answer_id', answer_id)
    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'type_':type_,
                'time':time_,
                'bReceive':bReceive,
                'file':file_,
                'chatType':chatType_
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        print('chat')
        message = event['message']
        type_ = event['type_']
        time_ = event['time']
        bReceive = event['bReceive']
        file_ = event['file']
        chatType_ = event['chatType']
        
        self.send(text_data=json.dumps({
            'message': message,
            'type':type_,
            'time':time_,
            'bReceive':bReceive,
            'file':file_,
            'chatType':chatType_
        }))
