from django.shortcuts import render
from school_app.models import Course
from silk.profiling.profiler import silk_profile

@silk_profile()
def main(request):
    courses = Course.objects.all()

    data = {
        "courses": courses[0:2],
    }
    return render(request, "main.html", data)