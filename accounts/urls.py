from rest_framework.routers import DefaultRouter
from accounts import views

router = DefaultRouter()
router.register('auth', views.UserViewSet, basename='auth')
router.register('forgot_password',views.ForgotViewset,basename='forgot_password')

urlpatterns = router.urls