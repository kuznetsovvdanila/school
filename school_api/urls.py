import django
import django.conf.urls.static
from django.urls import include, path
from rest_framework import routers

from school import settings
from . import views

urlpatterns = [
    path('course/', views.getCourse),
    path('course/lessons', views.getAllLessons),
    path('point/course/lesson', views.getLesson),
    path('point/course/lesson/task', views.getTask),
    path('user/auth', views.Authentication)
] + django.conf.urls.static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
