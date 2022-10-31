from django.urls import path

from . import views


urlpatterns = [
    path('', views.CourseList.as_view(), name='main'),
    path('<int:pk>', views.CourseInfo.as_view(), name='index'),
    path('<int:pk>/<int:pk2>', views.LessonInfo.as_view(), name='lesson'),
    path('<int:pk>/<int:pk2>/<int:pk3>', views.TaskInfo.as_view(), name='task')
]