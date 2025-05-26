from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.postgres.search import TrigramSimilarity

from task_manager.models import Task
from task_manager.serializers import TaskSerializers, TaskLightSerializer, TaskUpdateSerializer, \
    TaskPatchStatusSerializer


class TaskListAPIView(APIView):
    def get(self, request):
        task = Task.objects.filter()
        return Response(TaskLightSerializer(instance=task, many=True).data)


class TaskListModelViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializers

    def get_queryset(self):
        pass
        search_query = self.request.query_params.get('search')
        queryset = Task.objects.all()
        if search_query:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity('title', search_query)
            ).filter(similarity__gt=0.2).order_by('-similarity')
        return queryset


class TaskDetailUpdateDeleteAPIView(APIView):
    def patch(self, request, pk):
        task = Task.objects.filter(pk=pk)
        serializer = TaskPatchStatusSerializer(instance=task, data=request.data)
        serializer.is_valid(raise_exception=True)
        task.update(**serializer.validated_data)
        return Response("Good job!")

    def get(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        return Response(TaskLightSerializer(instance=task).data)

    def put(self, request, pk):
        task = Task.objects.filter(pk=pk)
        TaskUpdateSerializer(data=request.data).is_valid(raise_exception=True)
        task.update(**request.data)
        return Response({"message": "Good job!"}, status=201)

    def delete(self, request, pk):
        task = Task.objects.filter(pk=pk)
        task.delete()
        return Response("Your task delete!")


class TaskCreateAPIView(APIView):
    def post(self, request):
        serializer = TaskSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        Task.objects.create(**serializer.validated_data)
        return Response({"message": "Good job!"}, status=201)

# class TaskGenericViewSet(GenericViewSet, ListModelMixin):
#     model =Task
#     serializer_class = TaskSerializers
#     def get(self, request):
#         pass
