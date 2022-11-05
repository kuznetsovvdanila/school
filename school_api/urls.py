from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'course', views.CourseView, basename="course")


urlpatterns = [
    path('', include(router.urls)),
    path('course/', views.CourseView.as_view({'get': 'list'}))
]
