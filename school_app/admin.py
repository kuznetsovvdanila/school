from django.contrib import admin
from django.shortcuts import render, HttpResponseRedirect
from .models import *

class LessonAdmin(admin.ModelAdmin):
    fields = ('name', 'id_course')

class CourseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'description')
    change_form_template = "admin/change_progress.html"

    def change(self, request, obj):
        print(11111)
        self.message_user(request, 'Panic')
        chats = []
        for i in range(3):
            chats.append(Chat.create(name='hui' + str(i), url="_"))
            chats[i].save()
        obj.chat.add(chats[0])
        obj.value += 1
        obj.save()
        return super().change(request, obj)

admin.site.register(Tag)
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
