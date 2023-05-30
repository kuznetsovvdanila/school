from channels.generic.websocket import AsyncWebsocketConsumer
import json

GROUP_UPDATES = "updates"

class UpdatesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            GROUP_UPDATES,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            GROUP_UPDATES,
            self.channel_name
        )

    # Отправка измененного Lesson
    async def lesson_updated(self, event):
        await self.send(text_data=json.dumps(event['message']))

    # Отправка уведомления
    async def send_notification(self, event):
        notification = event['notification']
        recipient = event['recipient']
        if recipient == self.user.id:
            await self.send(text_data=json.dumps({
                'notification': notification.text,
                'created_at': notification.created_at.isoformat()
            }))

