from django.urls import path
from task_manager import views
from rest_framework.routers import DefaultRouter

from task_manager.views import ExportExelView

router = DefaultRouter()
router.register(
    'task', views.TaskViewSet, basename='task'
)
router.register('project', views.ProjectViewSet, basename='project')




urlpatterns = [
                  path('', views.HelloAPIView.as_view(), name='hello'),
                  path('project/', views.ProjectAPIView.as_view(), name='hello'),
                  path('project/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='hello'),
                  path('export-excel/', ExportExelView.as_view(), name='export-excel'),

              ]+router.urls
