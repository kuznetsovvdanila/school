from rest_framework import serializers

from school_app.models import *

class PushSerializer(serializers.ModelSerializer):
    class Meta:
        model = Push
        fields = ['created', 'content']

#   Support
class FileTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTask
        fields = ['name', 'file']

#   Support
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'text', 'index']

#   POST
#   4th Stage request to get CourseInfo = getTask
class TaskFileSerializer(serializers.ModelSerializer):
    files = FileTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['files']

#   Support
class HomeworkSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Homework
        fields = ['id', 'tasks']

#   Support
class FileLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileLesson
        fields = ['name', 'file']

#   Support
#   Lessons preload to courses Fragment
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'access', 'getTasks', 'index']

#   POST
#   3rd Stage request to get CourseInfo = getLesson
class LessonPoolSerializer(serializers.ModelSerializer):
    homework = HomeworkSerializer(many=False, read_only=True)
    files = FileLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['link', 'description', 'homework', 'files']

#   Support
class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id_course', 'is_bought', 'whole_course', 'lessons', 'status_tasks']

#   GET/POST
class UserSerializer(serializers.ModelSerializer):
    progresses = ProgressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'grade', 'email', 'phone_number', 'progresses', 'registered']

#   POST
class UserNotificationsSerializer(serializers.ModelSerializer):
    notifications = PushSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['notifications']

#   POST
class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']

#   Support
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'surname', 'description', 'avatar', ]

#   GET
#   1st Stage request to get CourseInfo = getCourse
class CourseSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'product_preview', 'value', 'lessonsCount', 
        'duration', 'date_open', 'teachers']

#   GET
#   2nd Stage request to get CourseInfo = getAllLesson
class CourseLessonPoolSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'lessons']
        
