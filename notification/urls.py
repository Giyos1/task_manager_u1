from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notification import views

router = DefaultRouter()
router.register('notification',views.NotificationViewSet,basename='notification')

urlpatterns = [
    path('',include(router.urls))
]