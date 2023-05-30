import os
from celery import Celery
from CONFIG import ENVIROMENTALPATH
from school.settings import develop

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.'+ENVIROMENTALPATH)

# Создание экземпляра Celery
app = Celery('school')

# Загрузка настроек из файла settings.py
app.config_from_object('django.conf:'+ENVIROMENTALPATH, namespace='CELERY')

# Автоматическое обнаружение и регистрация задач в приложениях Django
app.autodiscover_tasks(lambda: develop.INSTALLED_APPS)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from datetime import timedelta
    from django.utils import timezone
    from school_app.models import Lesson
    from school_app.tasks import update_lesson_access

    # Получаем уроки, у которых доступ закрыт
    lessons = Lesson.objects.filter(access=Lesson.accesses.closed)

    # Для каждого урока создаем периодическую задачу
    for lesson in lessons:
        # Рассчитываем интервал до времени начала урока минус 10 минут
        countdown = (lesson.date_to_start - timezone.now()) - timedelta(minutes=10)

        if countdown.total_seconds() > 0:
            # Запуск задачи с указанным интервалом
            sender.add_periodic_task(countdown, update_lesson_access.s(lesson.id), name=f'update_lesson_access_{lesson.id}')
