from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from consumers import GROUP_UPDATES
from models import Lesson, Notification

async def observe_lesson(lesson : Lesson):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        GROUP_UPDATES, {
            'type': 'lesson_updated',
            'message': {
                'id': lesson.id,
                'name': lesson.name,
                'description': lesson.description,
                # и т.д.
            }
        })
    

# Будущие уведомления 
# async def observe_notification(notification : Notification):
#     notification_data = {
#        'notification': notification.text,
#        'created_at': notification.created_at.isoformat()
#     }
#     await channel_layer.group_send(
#     "updates",
#     {
#         'type': 'send_notification',
#         'notification': notification_data,
#         'recipient': recipient.id,
#     }
# )