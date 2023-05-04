from django.conf.urls.static import static
from django.urls import include, path

from school.settings.base import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL
from .views import lk, main

urlpatterns = [
    path('', main.main, name='main'),
    path('personal_area', lk.lk, name='lk'),
] + static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

"""path('', views.CourseList.as_view(), name='main'),
    path('<int:pk>', views.CourseInfo.as_view(), name='index'),
    path('<int:pk>/<int:pk2>', views.LessonInfo.as_view(), name='lesson'),
    path('<int:pk>/<int:pk2>/<int:pk3>', views.TaskInfo.as_view(), name='task'),"""