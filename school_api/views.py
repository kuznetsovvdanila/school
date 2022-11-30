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

import logging

logging.basicConfig(level=logging.INFO, filename="pylog.log", format="%(pastime)s %(levelness)s %(message)s")


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

@api_view(("GET", "POST"))
def getCourses(request):
    context = list()

    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        if getApi is not None:

            if request.method == "GET":
                queryset = Course.objects.exclude(is_active=Course.condition.is_archive).order_by('date_open')
                serializer = CourseSerializer(instance=queryset, many=True)
                for i in range(len(queryset)):
                    context.append(dict())
                    context[i].update(serializer.data[i])
                return Response(context)

            if request.method == "POST":
                user_id = int(request.data.get("user_id"))
                user = User.objects.get(id=user_id)
                user_courses = user.progresses.all()
                user_courses_id = [user_course.id_course for user_course in user_courses]

                queryset = Course.objects.exclude(is_active=Course.condition.is_archive).exclude(pk__in=user_courses_id)
                serializer = CourseSerializer(instance=queryset, many=True)

                for i in range(len(queryset)):
                    context.append(dict())
                    context[i].update(serializer.data[i])
                return Response(context)

        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)

@api_view(("POST",))
def getMyCourses(request):
    context = list()

    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        if getApi is not None:

            user_id = int(request.data.get("user_id"))
            user = User.objects.get(id=user_id)
            user_courses = user.progresses.all().order_by("id")
            user_courses_id = [user_course.id_course for user_course in user_courses]

            queryset = Course.objects.exclude(is_active=Course.condition.is_archive).filter(pk__in=user_courses_id)
            serializer = MyCourseSerializer(instance=queryset, many=True)

            for i in range(len(queryset)):
                context.append(dict())
                context[i].update(serializer.data[i])
            return Response(context)

        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)

# Подгрузка после загрузки всех курсов, пост при авторизованном пользователе
@api_view(("GET", "POST"))
def getAllLessons(request):
    context = list()
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)

        if getApi is not None:
            if request.method == "GET":
                queryset = Course.objects.exclude(is_active=Course.condition.is_archive).order_by('date_open')
                serializer = CourseLessonPoolSerializer(instance=queryset, many=True)
                for i in range(len(queryset)):
                    context.append(dict())
                    context[i].update(serializer.data[i])
                return Response(context)

            if request.method == "POST":
                user_id = int(request.data.get("user_id"))
                user = User.objects.get(id=user_id)
                user_courses = user.progresses.all()
                user_courses_id = [user_course.id_course for user_course in user_courses]

                queryset = Course.objects.exclude(is_active=Course.condition.is_archive).exclude(pk__in=user_courses_id)
                serializer = CourseLessonPoolSerializer(instance=queryset, many=True)

                for i in range(len(queryset)):
                    context.append(dict())
                    context[i].update(serializer.data[i])
                return Response(context)
        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)


#   Подгрузка при заходе на урок
#   request ( body{ "course_id" : CourseID, "lesson_index" : LessonIndex } )
@api_view(("POST",))
def getLesson(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (course_id, lesson_index) = (int(request.data.get("course_id")),
                                     int(request.data.get("lesson_index")))
        if getApi is not None:
            course_instance = Course.objects.get(id=course_id)
            lesson = course_instance.lessons.get(index=lesson_index)
            serializer = LessonPoolSerializer(instance=lesson, many=False)
            return Response(serializer.data)
        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)


@api_view(("POST",))
def getLessonFiles(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (course_id, lesson_index) = (int(request.data.get("course_id")),
                                     int(request.data.get("lesson_index")))
        if getApi is not None:
            course_instance = Course.objects.get(id=course_id)
            lesson = course_instance.lessons.get(index=lesson_index)
            serializer = LessonFilesSerializer(instance=lesson, many=False)
            return Response(serializer.data)
        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)


#   Подгрузка при заходе на таск
#   request ( body{ "course_id" : CourseID, "lesson_index" : LessonIndex,  "task_index" : TaskIndex} )
@api_view(("POST",))
def getTaskFiles(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (course_id, lesson_index, task_index) = (int(request.data.get("course_id")),
                                                 int(request.data.get("lesson_index")),
                                                 int(request.data.get("task_index")))
        if getApi is not None:
            course_instance = Course.objects.get(id=course_id)
            lesson_instance = course_instance.lessons.get(index=lesson_index)
            task = lesson_instance.homework.tasks.get(index=task_index)
            serializer = TaskFilesSerializer(instance=task, many=False)
            return Response(serializer.data)
        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)


@api_view(("POST",))
def checkAnswer(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (user_id, course_id, lesson_index, task_index, answer) = (int(request.data.get("user_id")),
                                                                  int(request.data.get("course_id")),
                                                                  int(request.data.get("lesson_index")),
                                                                  int(request.data.get("task_index")),
                                                                  str(request.data.get("answer")))

        # logging.info("get values",user_id,course_id,lesson_index,task_index,answer)

        if getApi is not None:
            user = User.objects.get(id=user_id)
            course_instance = Course.objects.get(id=course_id)
            lesson_instance = course_instance.lessons.get(index=lesson_index)
            task = lesson_instance.homework.tasks.get(index=task_index)

            # logging.info("get instances", user,course_instance,lesson_instance,task)

            if not user.progresses.filter(id_course=course_id).exists():
                course_instance.addTrial(user=user)

                progress = Progress.create(course_instance)
                progress.save()

                user.progresses.add(progress)
                user.save()

            progress = user.progresses.get(id_course=course_id)
            progress.taskProgress(lesson_index, task_index, task.checkAnswer(user, answer), answer)

            serializer = UserProgressSerializer(instance=user, many=False)
            return Response(serializer.data)

        else:
            return Response(status_code=404)

    except KeyError:
        return Response(status=500)


#   Авторизация
#   request ( body{ "login" : login, "password" : password} )
@api_view(("POST",))
def Authentication(request):
    context = {}
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (login, password) = (request.data.get("login"),
                             request.data.get("password"))
        if getApi is not None:
            (check, user_instance, error_message) = authValid(login, password)
            if check:
                serializer = UserSerializer(instance=user_instance, many=False)
                serializerNotify = UserNotificationsSerializer(instance=user_instance, many=False)
                serializerProgresses = UserProgressSerializer(instance=user_instance, many=False)

                context.update(serializer.data)
                context.update(serializerNotify.data)
                context.update(serializerProgresses.data)

                return Response(context)
            else:
                return Response({'error_message': error_message})
        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)


#   Регистрация
#   request ( body{ "login" : login, "password" : password,  "password_complete" : password_c} )
@api_view(("POST",))
def Registration(request):
    context = {}
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]

        logging.info(request.data)

        getApi = APIKey.objects.get_from_key(key)
        (login, password) = (request.data.get("login"),
                             request.data.get("password"))

        if getApi is not None:
            (check, error_message, user) = regValid(login, password)
            if check:
                serializer = UserSerializer(instance=user, many=False)
                serializerNotify = UserNotificationsSerializer(instance=user, many=False)
                serializerProgresses = UserProgressSerializer(instance=user, many=False)

                context.update(serializer.data)
                context.update(serializerNotify.data)
                context.update(serializerProgresses.data)

                logging.info(f"{context}")

                return Response(context)
            return Response({"error_message": error_message})
        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)


#   Дополнительные данные о пользовате
#   request ( body{ "user_id": user_id, "name" : name, "surname" : surname,  "grade" : grade} )

# заполнение полей имени + остального после регистрации
@api_view(("POST",))
def UpdateInfoAboutUser(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        (user_id, name, surname, email, phone_number) = (
                                        request.data.get("user_id"),
                                        request.data.get("name"),
                                        request.data.get("surname"),
                                        request.data.get("email"),
                                        request.data.get("phone_number"))
        if getApi is not None:
            user_instance = User.objects.get(id=user_id)
            user_instance.name = name
            user_instance.surname = surname
            user_instance.email = email
            user_instance.phone_number = phone_number
            user_instance.save()
            response = {"user_id": user_id, "name": name, "surname": surname, "email": email, "phone_number": phone_number}
            return Response(response)
        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)


@api_view(("POST",))
def getProgresses(request):
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        user_id = (int(request.data.get("user_id")))

        if getApi is not None:
            user = User.objects.get(id=user_id)

            if user.progresses.exists():
                serializer = UserProgressSerializer(instance=user, many=False)
                return Response(serializer.data)
            else:
                error_message = "null"
                return Response({"error_message": error_message})

        else:
            return Response(status_code=404)

    except KeyError:
        return Response(status=500)

# wait for user_id if POST
@api_view(("GET", "POST"))
def getChats(request):
    context = list()
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        if getApi is not None:
            if request.method == "GET":
                queryset = Course.objects.exclude(is_active=Course.condition.is_archive)
                serializer = CourseChatsPoolSerializer(instance=queryset, many=True)
                return Response(serializer.data)

            elif request.method == "POST":
                user_id = int(request.data.get("user_id"))
                user = User.objects.get(id=user_id)
                user_progresses = user.progresses.all()
                user_courses_id = [user_progress.id_course for user_progress in user_progresses]

                queryset = Course.objects.exclude(is_active=Course.condition.is_archive).exclude(pk__in=user_courses_id)
                if len(queryset) != 0:
                    serializer = CourseChatsPoolSerializer(instance=queryset, many=True)
                    for i in range(len(queryset)):
                        context.append(dict())
                        context[i].update(serializer.data[i])
                    return Response(context)
        else:
            return Response(status_code=404)
    except KeyError:
        return Response(status=500)

@api_view(("POST",))
def getMyChats(request):
    context = list()
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        user_id = int(request.data.get("user_id"))
        if getApi is not None:
            user = User.objects.get(id=user_id)
            user_progresses = user.progresses.all()
            user_courses_id = [user_progress.id_course for user_progress in user_progresses]
            user_courses_id_accessed = [user_progress.id_course for user_progress in user_progresses if user_progress.is_bought]

            if len(user_courses_id) != 0:
                queryset = Course.objects.exclude(is_active=Course.condition.is_archive).filter(pk__in=user_courses_id)
                accessed_queryset = queryset.filter(pk__in=user_courses_id_accessed)
                if accessed_queryset.exists():
                    print(accessed_queryset)
                    accessed_serializer = AccessedCourseChatsPoolSerializer(instance=accessed_queryset, many=True)
                    counter = 0
                    for i in range(len(accessed_queryset)):
                        context.append(dict())
                        context[i].update(accessed_serializer.data[i])
                        counter = i+1
                    if len(user_courses_id) != len(user_courses_id_accessed):
                        exclude_accessed = queryset.exclude(pk__in=user_courses_id_accessed)
                        serializer = CourseChatsPoolSerializer(instance=exclude_accessed)
                        for i in range(len(exclude_accessed)):
                            context.append(dict())
                            context[counter+i].update(serializer.data[i])
                    return Response(context)
                else:
                    print(queryset)
                    serializer = CourseChatsPoolSerializer(instance=queryset, many=True)
                    for i in range(len(queryset)):
                        context.append(dict())
                        context[i].update(serializer.data[i])
                    return Response(context)
            else: 
                return Response(status=300)
        else:
            return Response(status=404)
    except KeyError:
        return Response(status=500)
