from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    context = {'pivo': 'tozepivo'}
    if request.method == 'GET':
        print('hello Percy')
        print(request.GET)
    elif request.method == 'POST':
        print(request.POST.get('name'))
        print(1)
    return render(request, 'index.html', context)
