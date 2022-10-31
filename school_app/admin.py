from django.contrib import admin
from .models import *

class LessonAdmin(admin.ModelAdmin):
    fields = ('name', 'id_course')

class CourseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'description')

admin.site.register(Push)
admin.site.register(FileTask)
admin.site.register(FileLesson)
admin.site.register(Task)
admin.site.register(Homework)
admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Chat)
admin.site.register(Course, CourseAdmin)
admin.site.register(Admin)
admin.site.register(SuperUser)
