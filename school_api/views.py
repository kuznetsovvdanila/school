from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from school_app.models import *
from .serializers import *


class CourseView(ViewSet):

    # @action(detail=False, methods=['get', 'post'], name="listed")
    def list(self, request):
        print(request.POST)
        queryset = Course.objects.all().order_by('name')
        serializer = CourseSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        print(request.POST)
        queryset = Course.objects.all().order_by('name')
        serializer = CourseSerializer(instance=queryset, many=True)
        return Response(serializer.data)

