from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.csrf import csrf_failure
from django.views.generic import DetailView, ListView, View
from .models import Course, Lesson, User
from django.contrib.auth import authenticate, login, logout, user_logged_in, get_user

from email_validate import validate
import re

# возвращает bool и User
def authValid(login : str, password : str) -> tuple:
    truth = False
    user_instance = None
    isUser = False
    if str(login).count("@") == 1:
        isUser = User.objects.filter(email=login).exists()
        user_instance = User.objects.get(email=login)
        if isUser:
            if (user_instance.check_password(password)):
                truth = True
    else:
        isUser = User.objects.filter(phone_number=login).exists()
        user_instance = User.objects.get(phone_number=login)
        if isUser:
            if (user_instance.check_password(password)):
                truth = True
    return truth, user_instance

# возвращает tuple(check : bool, error_message : string, User.id : int)
def regValid(login : str, password : str, password_complete : str) -> tuple:
    truth = False
    error_message = ""
    user_instance = None

     # Проверяем на соответствие поля "email"у
    if list(login).count("@"):
        isUser : bool = User.objects.filter(email=login).exists()
        if not(isUser):
            if password == password_complete:
                user_instance = User(email=login, password=password)
                user_instance.save()
                truth = True
        else:
            error_message = "Пользователь с таким email адресом уже существует"

    # Проверяем на соответствие поля телефонному номеру
    elif re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', login):
        isUser : bool = User.objects.filter(phone_number=login).exists()
        if not(isUser):
            if password == password_complete:
                user_instance = User(phone_number=login, password=password)
                user_instance.save()
                truth = True
        else:
            error_message = "Пользователь с таким номером мобильного телефона уже существует"
    else:
        error_message = "Login не соответствует существующему email или номеру мобильного телефона"
    return (truth, error_message, user_instance)

class CourseList(View):

    def get(self, request):
        courses = Course.objects.all()
        return render(request, "main.html", {"courses": courses})

class CourseInfo(View):
    
    def get(self, request, pk):
        course = Course.objects.get(id=pk)
        lessons = course.lessons.all()
        return render(request, "course.html", {"course": course, "lessons": lessons})

class LessonInfo(View):

    def get(self, request, pk, pk2):
        course = Course.objects.get(id=pk)
        lesson = course.lessons.get(id=pk2)
        tasks = lesson.homework.tasks.all()
        return render(request, "lesson.html", {"course": course, "lesson": lesson, "tasks": tasks})

class TaskInfo(View):

    def get(self, request, pk, pk2, pk3):
        user = User.objects.get(id=0)
        login(request, user)
        course = Course.objects.get(id=pk)
        lesson = course.lessons.get(id=pk2)
        task = lesson.homework.tasks.get(id=pk3)
        return render(request, "task.html", {"task": task})
    
    def post(self, request, pk, pk2, pk3):
        course = Course.objects.get(id=pk)
        lesson = course.lessons.get(id=pk2)
        task = lesson.homework.tasks.get(id=pk3)
        context = {"task": task}

        user = request.user
        answer = request.POST.get(name="answer")
        path = request.path
        print(user.id)
        boolean = task.check_answer(user=user, answer=answer, path=path)

        context.update({"bool": boolean})
        return render(request, "task.html", context)