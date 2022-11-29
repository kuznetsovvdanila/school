from rest_framework import serializers

from school_app.models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
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
class TaskFilesSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Lesson
        fields = ['link', 'description', 'homework']

class LessonFilesSerializer(serializers.ModelSerializer):
    files = FileLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['files']

#   Support
class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id_course', 'is_bought', 'whole_course', 'lessons', 'status_tasks', 'answer_tasks']

#POST
class UserProgressSerializer(serializers.ModelSerializer):
    progresses = ProgressSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ["progresses"]

#   GET/POST
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'grade', 'email', 'phone_number', 'registered_datetime']

#   POST
class UserNotificationsSerializer(serializers.ModelSerializer):
    notifications = NotificationsSerializer(many=True, read_only=True)

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

#   Support
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['name', 'url']

#   Support
class ChatImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['image']

#   GET
#   1st Stage request to get CourseInfo = getCourse
class CourseSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    chat = ChatSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'product_preview', 'description', 'value', 'lessonsCount',
        'duration', 'date_open', 'teachers', 'tags', 'chat']

#   GET
#   2nd Stage request to get CourseInfo = getAllLesson
class CourseLessonPoolSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'lessons']

class CourseChatsPoolSerializer(serializers.ModelSerializer):
    chats = ChatImageSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['chats']

class MyLessonSerializer(serializers.ModelSerializer):  #full lesson
    homework = HomeworkSerializer(many=False, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'access', 'getTasks', 'index', 'link', 'description', 'homework']

class MyCourseSerializer(serializers.ModelSerializer): #full course
    teachers = TeacherSerializer(many=True, read_only=True)
    lessons = MyLessonSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    chat = ChatSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'product_preview', 'description', 'value', 'lessonsCount', 
                    'duration', 'date_open', 'teachers', 'lessons', 'tags', 'chat']


