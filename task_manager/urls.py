from django.urls import path
from task_manager.views import ProjectAPIView, ProjectDetailAPIView, TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path('projects/', ProjectAPIView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('projects/<int:project_pk>/tasks/', TaskListAPIView.as_view(), name='project-tasks'),
]