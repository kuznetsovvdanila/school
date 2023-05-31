from celery import shared_task
from django.utils import timezone
from .models import Lesson
from school_app.models import Lesson
from school_app.tasks import update_lesson_access
from datetime import timedelta
from .__init__ import celery_app

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Получаем уроки, у которых доступ закрыт
    lessons = Lesson.objects.filter(access=Lesson.accesses.closed)

    # Для каждого урока создаем периодическую задачу
    for lesson in lessons:
        # Рассчитываем интервал до времени начала урока минус 10 минут
        countdown = (lesson.date_to_start - timezone.now()) - timedelta(minutes=10)

        if countdown.total_seconds() > 0:
            # Запуск задачи с указанным интервалом
            sender.add_periodic_task(countdown, update_lesson_access.s(lesson.id), name=f'update_lesson_access_{lesson.id}')

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
