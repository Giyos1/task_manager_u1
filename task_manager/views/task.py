from rest_framework.response import Response
from rest_framework.views import APIView

from task_manager.models import Task
from task_manager.serializers import TaskCreateSerializers, TaskLightSerializer, TaskUpdateSerializer, \
    TaskPatchStatusSerializer


class TaskListAPIView(APIView):
    def get(self, request):
        task = Task.objects.filter()
        return Response(TaskLightSerializer(instance=task, many=True).data)


class TaskDetailUpdateDeleteAPIView(APIView):
    def patch(self, request, pk):
        task = Task.objects.filter(pk=pk)
        if not task:
            return Response("Not found this task!")
        serializer = TaskPatchStatusSerializer(instance=task, data=request.data)
        serializer.is_valid(raise_exception=True)
        task.update(**serializer.validated_data)
        return Response("Good job!")

    def get(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        if not task:
            return Response("Not found this task")
        return Response(TaskLightSerializer(instance=task).data)

    def put(self, request, pk):
        task = Task.objects.filter(pk=pk)
        if not task:
            return Response("Not found this task")
        TaskUpdateSerializer(data=request.data).is_valid(raise_exception=True)
        task.update(**request.data)
        return Response({"message": "Good job!"}, status=201)

    def delete(self, request, pk):
        task = Task.objects.filter(pk=pk)
        if not task:
            return Response("This task not found")
        task.delete()
        return Response("Your task delete!")


class TaskCreateAPIView(APIView):
    def post(self, request):
        serializer = TaskCreateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        Task.objects.create(**serializer.validated_data)
        return Response({"message": "Good job!"}, status=201)

#
# {
# "title":"salom",
# "status":"to_do",
# "project":1,
# "user":1
# }
