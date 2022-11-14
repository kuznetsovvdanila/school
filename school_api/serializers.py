from rest_framework import serializers

from school_app.models import *

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'product_preview', 'value', 'lessonsCount', 
        'duration', 'date_open', 'lessons', ]
        
