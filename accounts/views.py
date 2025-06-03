from django.contrib.auth import login, logout
from rest_framework.decorators import action
from rest_framework.mixins import  CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from accounts.models import User
from accounts.serializers import UserRegisterSerializer, LoginSerializer, UserLightSerializer, CheckUserSerializer, \
    RestoreSerializer
from accounts.service import create_token, refresh_token


class UserViewSet(GenericViewSet,CreateModelMixin):
    queryset = User.objects.all()
    serializer_class =UserRegisterSerializer
    permission_classes = [AllowAny]


    def get_permissions(self):
        if self.action in ['logout_token','session']:
            return [IsAuthenticated()]
        return super().get_permissions()


    def get_serializer_class(self):
        if self.action in ['login','login_with_token']:
            return LoginSerializer
        return self.serializer_class



    @action(methods=['post'],detail=False)
    def login(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        login(request, user)
        return Response({"message": "ok"})

    @action(methods=['post'],detail=False)
    def login_with_token(self,request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data.get('user')
        token = create_token(user.id)
        return Response(token)


    @action(methods=['post'],detail=False)
    def refresh_access_token(self,request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({'error':'Refresh token is required'}, status=400)
        result = refresh_token(refresh)
        if 'error' in result:
            return Response(result,status=401)
        return Response(result)






    @action(methods=['delete'],detail=False)
    def logout_token(self,request):
        request.user.auth_token.delete()
        return Response({'message':'ok'})


    @action(methods=['get'],detail=False)
    def session(self,request):
        user = request.user
        serializers = UserLightSerializer(user)
        return Response(data=serializers.data)





class ForgotViewset(GenericViewSet,CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RestoreSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CheckUserSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Emailga code muvaffaqiyatli yuborildi'}, status=201)


    @action(methods=['post'],detail=False,serializer_class=RestoreSerializer)
    def restore_password(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'password muvofaqiyatli tiklandi'})
