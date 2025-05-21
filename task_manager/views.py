from rest_framework.response import Response
from rest_framework.views import APIView
from task_manager.models.project import Project
from task_manager.models.task import Task
from .serializers import ProjectListSerializer, ProjectCreateAndUpdateSerializer, ProjectDetailSerializer, TaskListSerializer, TaskCreateAndUpdateSerializer

class ProjectAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            project = Project.objects.get(id=pk)
            serializer = ProjectDetailSerializer(project)
        else:
            projects = Project.objects.all()
            serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectCreateAndUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        Project.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            product_owner=data.get('product_owner')
        )
        return Response({"message": "Project created"}, status=201)

class ProjectDetailAPIView(APIView):
    def get(self, request, pk):
        project = Project.objects.get(id=pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = Project.objects.get(id=pk)
        serializer = ProjectCreateAndUpdateSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        project.name = data.get('name', project.name)
        project.description = data.get('description', project.description)
        project.product_owner = data.get('product_owner', project.product_owner)
        project.save()
        return Response({"message": "Project updated"}, status=200)

    def delete(self, request, pk):
        project = Project.objects.get(id=pk)
        project.delete()
        return Response({"message": "Project deleted"}, status=204)

class TaskListAPIView(APIView):
    def get(self, request, project_pk=None, status=None):
        if project_pk:
            tasks = Task.objects.filter(project_id=project_pk)
        else:
            tasks = Task.objects.all()
        if status:
            tasks = tasks.filter(status=status)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskCreateAndUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            Task.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                status=data.get('status'),
                assigned_to=data.get('assigned_to'),
                reviewer=data.get('reviewer'),
                project=data.get('project')
            )
            return Response({"message": "Task created"}, status=201)
        return Response(data=serializer.errors, status=400)

class TaskDetailAPIView(APIView):
    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        serializer = TaskListSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = Task.objects.get(id=pk)
        serializer = TaskCreateAndUpdateSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.assigned_to = data.get('assigned_to', task.assigned_to)
        task.reviewer = data.get('reviewer', task.reviewer)
        task.project = data.get('project', task.project)
        task.save()
        return Response({"message": "Task updated"}, status=200)

    def delete(self, request, pk):
        task = Task.objects.get(id=pk)
        task.delete()
        return Response({"message": "Task deleted"}, status=204)