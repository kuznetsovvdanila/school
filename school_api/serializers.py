from rest_framework import serializers

from school_app.models import *

class CourseSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
