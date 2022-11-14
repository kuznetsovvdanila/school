from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.csrf import csrf_failure
from django.views.generic import DetailView, ListView, View
from .models import Course, Lesson, User
from django.contrib.auth import authenticate, login, logout, user_logged_in, get_user

# def main(request):
#     context = {'pivo': 'tozepivo'}
#     if request.method == 'POST':
#         print(request.POST.get('name'))
#     courses = Course.objects.all()
#     teacher = courses[0].teachers.all()[0]
#     context.update({"teacher": teacher,
#                     "courses": courses})

#     #path = /idCourse_nameCourse/indexLesson_nameLesson/indexTask
#     # course = Course.objects.create()
#     # course = Course.create(*args)
#     print(request.path)
#     return render(request, 'main.html', context)

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