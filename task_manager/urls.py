from django.urls import path
from task_manager import views

urlpatterns = [
    path('', views.HelloAPIView.as_view(), name='hello'),
    path('project/', views.ProjectAPIView.as_view(), name='hello'),
    path('project/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='hello'),
    path('project/list/<int:pk>/', views.ProjectListAPIView.as_view(), name='hello'),
]

urlpatterns += [
    path('task/create/', views.TaskCreateAPIView.as_view(), name='task_create'),
    path('task/list/<int:pk>', views.TaskListAPIView.as_view(), name='task_list'),
    path('task/<int:pk>/', views.TaskDetailUpdateDeleteAPIView.as_view(), name='task'),
    # path('task/update/<int:pk>/', TaskUpdateAPIView.as_view(), name='task_update'),
]

# change