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
