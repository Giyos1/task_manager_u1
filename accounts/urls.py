from django.urls import path
from accounts import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    'create', views.UserCreateGenericViewSet, basename='user_create',
)

urlpatterns = [

              ] + router.urls
