from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_api_key.models import APIKey
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.serializers import ListSerializer

from school_app.models import *
from .serializers import *


# class CourseView(ViewSet):

#     # @action(detail=False, methods=['get', 'post'], name="listed")
#     def list(self, request):
#         queryset = Course.objects.all().order_by('name')
#         serializer = CourseSerializer(instance=queryset, many=True)
#         http = self.create(request)
#         return http

#     def create(self, request):
#         try:
#             key = request.META["HTTP_AUTHORIZATION"].split()[0]
#             APIKey.objects.get_from_key(key)
#             queryset = Course.objects.all().order_by('name')
#             serializer = CourseSerializer2(instance=queryset, many=True)
#             return Response(serializer.data)
#         except KeyError:
#             return Response(status=500)

@api_view(("GET", "POST"))
def getCourse(request):
    context = list()
    try:
        key = request.META["HTTP_AUTHORIZATION"].split()[0]
        getApi = APIKey.objects.get_from_key(key)
        if getApi is not None:
            queryset = Course.objects.all().order_by('name')
            serializer = CourseSerializer(instance=queryset, many=True)
            serializerm2m = CourseSerializerM2m(instance=queryset, many=True)
            for i in range(len(serializer.data)):
                context.append(dict())
                context[i].update(serializer.data[i])
                context[i].update(serializerm2m.data[i])
            return Response(context)
        else: return Response(status_code=404)
    except KeyError:
        return Response(status=500)