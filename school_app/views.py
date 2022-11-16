from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.csrf import csrf_failure
from django.views.generic import DetailView, ListView, View
from .models import Course, Lesson, User
from django.contrib.auth import authenticate, login, logout, user_logged_in, get_user

from django.core.validators import email_re
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
import re

# возвращает bool и User
def authValid(login : str, password : str) -> tuple:
    truth = False
    user_instance = None
    if str(login).count("@") == 1:
        user_instance = User.objects.get(email=login)
    else:
        user_instance = User.objects.get(phone_number=login)
    if user_instance is not None:
        if (user_instance.check_password(password)):
            truth = True
    return truth, user_instance

# возвращает tuple(check : bool, error_message : string, User.id : int)
def regValid(login : str, password : str, password_complete : str) -> tuple:
    truth = False
    error_message = ""
    user_instance = None

     # Проверяем на соответствие поля "email"у
    if email_re.search(smart_unicode(login)):
        user_instance = User.objects.get(email=login)
        if user_instance is None:
            if password == password_complete:
                user_instance = User(email=login, password=password)
                user_instance.save()
        else:
            error_message = "Пользователь с таким email адресом уже существует"

    # Проверяем на соответствие поля телефонному номеру
    elif re.compile("^([0-9\(\)\/\+ \-]*)$").search(smart_unicode(login)):
        user_instance = User.objects.get(phone_number=login)
        if user_instance is None:
            if password == password_complete:
                user_instance = User(email=login, password=password)
                user_instance.save()
        else:
            error_message = "Пользователь с таким номером мобильного телефона уже существует"
    else:
        error_message = "Login не соответствует существующему email или номеру мобильного телефона"
    return (truth, error_message, (user_instance.id if user_instance is not None else None))

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