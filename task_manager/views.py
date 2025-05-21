from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from task_manager.models import Project, Task
from task_manager.Serializers import ProjectListSerializer, ProjectDetailSerializers, ProjectCreateAndUpdateSerializers, \
TaskListSerializer, TaskCreateAndUpdateSerializer, TaskDetailSerializer


# class HelloAPIView(APIView):
#     def get(self, request):
#         return Response({
#             'message': 'Hello World'
#         })
#


class ProjectAPIView(APIView):
    def get(self, request, pk=None):
        projects = Project.objects.all()
        serializers = ProjectListSerializer(projects, many=True)
        return Response(data=serializers.data)

    def post(self, request):
        serializer = ProjectCreateAndUpdateSerializers(data=request.data, context={'request': request})
        # if serializer.is_valid():
        #     data = serializer.validated_data
        #     Project.objects.create(
        #         name=data.get('name'),
        #         description=data.get('description'),
        #         owner=data.get('owner')
        #     )
        #     return Response({"message": "ok"}, status=201)
        # return Response(data=serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        Project.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            owner=data.get('owner')
        )
        return Response({"message": "ok"}, status=201)


class ProjectDetailAPIView(APIView):
    def get(self, request, pk):
        project = Project.objects.filter(id=pk).first()
        serializer = ProjectDetailSerializers(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = Project.objects.filter(id=pk).first()
        serializer = ProjectCreateAndUpdateSerializers(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            project.name = data.get('name')
            project.description = data.get('description')
            project.owner = data.get('owner')
            project.save()
            return Response({"message": "ok"}, status=201)
        return Response(data=serializer.errors, status=400)


class TaskAPIView(APIView):
    def get(self,request):
        tasks = Task.objects.all()
        serializers = TaskListSerializer(tasks)
        return Response(serializers.data,status=201)


    def post(self,request):
        serializer =TaskCreateAndUpdateSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=201)






class TaskDetailAPIView(APIView):
    def get(self,request,pk):
        task =get_object_or_404(Task)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data,status=201)


    def put(self,request,pk):
        task = Task.objects.filter(id=pk)
        serializer = TaskCreateAndUpdateSerializer(instance=task,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=201)

