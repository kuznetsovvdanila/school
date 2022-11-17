import django.conf.urls.static
from django.urls import include, path
from rest_framework import routers

from school import settings
from . import views

urlpatterns = [
    path('', views.CourseList.as_view(), name='main'),
    path('<int:pk>', views.CourseInfo.as_view(), name='index'),
    path('<int:pk>/<int:pk2>', views.LessonInfo.as_view(), name='lesson'),
    path('<int:pk>/<int:pk2>/<int:pk3>', views.TaskInfo.as_view(), name='task'),
] + django.conf.urls.static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)