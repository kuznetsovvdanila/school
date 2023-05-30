from celery import shared_task
from django.utils import timezone
from .models import Lesson

# Необходима проверка возможности сменить поле / заранее отправить админу информацию о том что урок не готов
@shared_task
def update_lesson_access(lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return

    current_time = timezone.now()

    if lesson.date_to_start - current_time <= timezone.timedelta(minutes=10):
        lesson.access = Lesson.accesses.partavailable
        lesson.save()
