from django.urls import include, path
from rest_framework import routers

from . import views

urlpatterns = [
    path('course/', views.getCourse),
    path('course/lessons', views.getAllLessons),
    path('point/course/lesson', views.getLesson),
    path('point/course/lesson/task', views.getTask)
]
