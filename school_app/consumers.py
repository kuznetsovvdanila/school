from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LessonConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "lesson_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "lesson_updates",
            self.channel_name
        )

    async def lesson_updated(self, event):
        await self.send(text_data=json.dumps(event['message']))
