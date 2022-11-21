from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_api_key.models import APIKey
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.serializers import ListSerializer

from school_app.models import *
from school_app.views import *
from .serializers import *


# class CourseView(ViewSet):

#     # @action(detail=False, methods=['get', 'post'], name="listed")
#     def list(self, request):
#         queryset = Course.objects.all().order_by('name')
#         serializer = CourseSerializer(instance=queryset, many=True)
#         http = self.create(request)
#         return http

#     def create(self, request):
#         try:
#             key = request.META["HTTP_AUTHORIZATION"].split()[0]
#             APIKey.objects.get_from_key(key)
#             queryset = Course.objects.all().order_by('name')
#             serializer = CourseSerializer2(instance=queryset, many=True)
#             return Response(serializer.data)
#         except KeyError:
#             return Response(status=500)

@api_view(("GET",))
def getCourse(request):
    context = list()
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        if getApi is not None:
            queryset = Course.objects.exclude(is_active = Course.condition.is_archive).order_by('date_open')
            serializer = CourseSerializer(instance=queryset, many=True)
            for i in range(len(queryset)):
                context.append(dict())
                context[i].update(serializer.data[i])
            return Response(context)
        else: return Response(status_code=404)
    except KeyError:
        return Response(status=500)

@api_view(("GET",))
def getAllLessons(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        if getApi is not None:
            queryset = Course.objects.exclude(is_active = Course.condition.is_archive).order_by('date_open')
            serializer = CourseLessonPoolSerializer(instance=queryset, many=True)
            return Response(serializer.data)
        else: return Response(status_code=404)
    except KeyError:
        return Response(status=500)

#   Подгрузка при заходе на урок
#   request ( body{ "course_id" : CourseID, "lesson_index" : LessonIndex } )
@api_view(("POST",))
def getLesson(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (course_id, lesson_index) = (int(request.POST.get("course_id")), int(request.POST.get("lesson_index")))
        if getApi is not None:
            course_instance = Course.objects.get(id=course_id)
            lesson = course_instance.lessons.get(index=lesson_index)
            serializer = LessonPoolSerializer(instance=lesson, many=False)
            return Response(serializer.data)
        else: return Response(status_code=404)
    except KeyError:
        return Response(status=500)

#   Подгрузка при заходе на таск
#   request ( body{ "course_id" : CourseID, "lesson_index" : LessonIndex,  "task_index" : TaskIndex} )
@api_view(("POST",))
def getTask(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (course_id, lesson_index, task_index) = (int(request.POST.get("course_id")), 
        int(request.POST.get("lesson_index")), int(request.POST.get("task_index")))
        if getApi is not None:
            course_instance = Course.objects.get(id=course_id)
            lesson_instance = course_instance.lessons.get(index=lesson_index)
            task = lesson_instance.homework.tasks.get(index=task_index)
            serializer = TaskFileSerializer(instance=task, many=False)
            return Response(serializer.data)
        else: return Response(status_code=404)
    except KeyError:
        return Response(status=500)

#   Авторизация
#   request ( body{ "login" : login, "password" : password} )
@api_view(("POST",))
def Authentication(request):
    context = [{}]
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (login, password) = (request.POST.get("login"), request.POST.get("password"))
        if getApi is not None:
            (check, user_instance) = authValid(login, password)
            if check:
                serializer = UserSerializer(instance=user_instance, many=False)
                serializerNotify = UserNotificationsSerializer(instance=user_instance, many=False)
                context[0].update(serializer.data)
                context[0].update(serializerNotify.data)
                return Response(context)
            else : return Response(status_code=203)
        else: return Response(status_code=404)
    except KeyError:
        return Response(status=500)

#   Регистрация
#   request ( body{ "login" : login, "password" : password,  "password_complete" : password_c} )
@api_view(("POST",))
def Registration(request):
    context = [{}]
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (login, password, password_complete) = (request.POST.get("login"),
            request.POST.get("password"), request.POST.get("password_complete"))
        if getApi is not None:
            (check, error_message, user) = regValid(login, password, password_complete)
            if check:
                serializer = UserSerializer(instance=user, many=False)
                serializerNotify = UserNotificationsSerializer(instance=user, many=False)
                context[0].update(serializer.data)
                context[0].update(serializerNotify.data)
                return Response(context)
            return Response({"error_message": error_message})
        else: return Response(status_code=404)
    except KeyError:
        return Response({"error_message": "error occurred"}, status=500)

#   Дополнительные данные о пользовате
#   request ( body{ "user_id": user_id, "name" : name, "surname" : surname,  "grade" : grade} )
@api_view(("POST",))
def UpdateInfoAboutUser(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (user_id, name, surname, grade) = (request.POST.get("user_id"), request.POST.get("name"),
            request.POST.get("surname"), request.POST.get("grade"))
        if getApi is not None:
            user_instance = User.objects.get(id=user_id)
            user_instance.name = name
            user_instance.surname = surname
            user_instance.grade = grade
            user_instance.save()
            response = {"name": name, "surname": surname, "grade": grade}
            return Response(response)
        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)

@api_view(("GET",))
def UpdateInfoAboutUserTest(request):
    context = [{}]
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        if getApi is not None:
            queryset = User.objects.all()[0]
            serializer = UserSerializer(instance=queryset, many=False)
            serializerNotify = UserNotificationsSerializer(instance=queryset, many=False)
            context[0].update(serializer.data)
            context[0].update(serializerNotify.data)
            return Response(context)

        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)