import django
import django.conf.urls.static
from django.urls import include, path
from rest_framework import routers

from school.settings.base import STATIC_URL, STATIC_ROOT
from . import views

urlpatterns = [
    path('course', views.getCourses),
    path('course/lessons', views.getAllLessons),
    path("course/chats", views.getChats),
    path('point/course/lesson', views.getLesson),
    path('point/course/lesson/task/files', views.getTaskFiles),
    path('user/auth', views.Authentication),
    path('user/reg', views.Registration),
    path("user/update", views.UpdateInfoAboutUser),
    path("point/course/lesson/files", views.getLessonFiles),
    path("task/answer", views.checkAnswer),
    path("user/progresses", views.getProgresses),
    path("course/self", views.getMyCourses),
    path("course/chats/self", views.getMyChats),

] + django.conf.urls.static.static(STATIC_URL, document_root=STATIC_ROOT)