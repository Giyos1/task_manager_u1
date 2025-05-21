from django.urls import path
from task_manager import views
from task_manager.views import TaskListAPIView, TaskDetailAPIView, TaskUpdateAPIView

urlpatterns = [
    path('', views.HelloAPIView.as_view(), name='hello'),
    path('project/', views.ProjectAPIView.as_view(), name='hello'),
    path('project/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='hello'),
]

urlpatterns += [
    path('task/create/', views.TaskCreateAPIView.as_view(), name='task_create'),
    path('task/list/api/', TaskListAPIView.as_view(), name='task_list'),
    path('task/detail/<int:pk>/', TaskDetailAPIView.as_view(), name='task_list'),
    path('task/update/<int:pk>/', TaskUpdateAPIView.as_view(), name='task_update'),
]
