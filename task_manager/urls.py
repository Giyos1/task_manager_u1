from django.urls import path

from task_manager import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    'search', views.TaskListModelViewSet, basename='task_list_search',
)
router.register(
    'project/search', views.ProjectListModelViewSet, basename='project_search'
)


urlpatterns = [
    path('', views.HelloAPIView.as_view(), name='hello'),
    path('project/', views.ProjectAPIView.as_view(), name='hello'),
    path('project/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='hello'),
    path('project/list/<int:pk>/', views.ProjectListAPIView.as_view(), name='hello'),
]

urlpatterns += [
    path('task/create/', views.TaskCreateAPIView.as_view(), name='task_create'),
    path('task/list/', views.TaskListAPIView.as_view(), name='task_list'),
    # path('task/list/search/', views.TaskListModelViewSet.as_view(), name='task_list_search'),

    path('task/<int:pk>/', views.TaskDetailUpdateDeleteAPIView.as_view(), name='task'),
    # path('task/update/<int:pk>/', TaskUpdateAPIView.as_view(), name='task_update'),
] + router.urls

# change