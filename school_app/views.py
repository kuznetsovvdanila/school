from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.csrf import csrf_failure
from .models import Course

def index(request):
    context = {'pivo': 'tozepivo'}
    if request.method == 'GET':
        print('hello Percy')
        print(request.GET)
    elif request.method == 'POST':
        print(request.POST.get('name'))
        print(request.path_info)

    #path = /idCourse_nameCourse/indexLesson_nameLesson/indexTask
    # course = Course.objects.create()
    # course = Course.create(*args)
    return render(request, 'index.html', context)

def csrf_failure(request, reason=""):
    context = {'pivo': 'otsosite chlen'}
    if request.method == 'POST':
        print(request.POST.get('name'))
        print('я прошел сквозь стену')
    return render(request, 'index.html', context)