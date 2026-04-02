import json
import base64
import uuid
import os

from google import genai
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.conf import settings
from chats.Ais import artificial_intelligence

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").split(",")
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope['user']

        user_message = await self.save_user_message(
            user=user,
            chat_id=self.chat_id,
            text=data.get('message', ''),
            file_data=data.get('file'),
            filename=data.get('filename'),
            for_ai=data.get('for_AI', False),
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_type': 'user',
                'text': user_message.text,
                'file_url': user_message.file.url if user_message.file else None,
                'filename': data.get('filename'),
                'user': user.username,
                'avatar_url': user.photo_profil.url if hasattr(user, 'photo_profil') and user.photo_profil else None,
                'message_id': user_message.id,
                'timestamp': user_message.created_at.isoformat(),
            }
        )

        if data.get('for_AI', False):
            await self.get_ai_response(
                chat_id=self.chat_id,
                user_text=user_message.text,
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))


    async def get_ai_response(self, chat_id, user_text):
        history = await self.get_chat_history(chat_id)

        ai_text = await sync_to_async(artificial_intelligence)(text=user_text)


        ai_message = await self.save_ai_message(
            chat_id=chat_id,
            text=ai_text,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_type': 'ai',
                'text': ai_text,
                'file_url': None,
                'user': 'Gemini',
                'message_id': ai_message.id,
                'timestamp': ai_message.created_at.isoformat(),
            }
        )


    @database_sync_to_async
    def save_user_message(self, user, chat_id, text, file_data=None, filename=None, for_ai=False):
        from .models import TogetherChat, MessageInChat

        chat = TogetherChat.objects.get(id=chat_id)
        message = MessageInChat(
            chat=chat,
            sender=user,
            text=text or '',
            is_AI=False,
            for_AI=for_ai,
        )

        if file_data:
            if ',' in file_data:
                file_data = file_data.split(',', 1)[1]
            file_bytes = base64.b64decode(file_data)
            ext = os.path.splitext(filename)[1] if filename else ''
            unique_name = f"{uuid.uuid4().hex}{ext}"
            message.save()
            message.file.save(unique_name, ContentFile(file_bytes), save=True)
        else:
            message.save()

        return message

    @database_sync_to_async
    def save_ai_message(self, chat_id, text):
        from .models import TogetherChat, MessageInChat

        chat = TogetherChat.objects.get(id=chat_id)
        return MessageInChat.objects.create(
            chat=chat,
            sender=None,
            text=text,
            is_AI=True,
            for_AI=False,
        )

    @database_sync_to_async
    def get_chat_history(self, chat_id):
        """Повертає історію у форматі Gemini (role: user/model)."""
        from .models import MessageInChat

        messages = (
            MessageInChat.objects
            .filter(chat__id=chat_id)
            .order_by('created_at')
        )

        history = []
        for msg in messages:
            role = 'model' if msg.is_AI else 'user'
            if msg.text:
                history.append({'role': role, 'parts': [msg.text]})

        return history