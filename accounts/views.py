from argparse import Action
from logging import raiseExceptions
from pickle import FALSE

from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import  CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from accounts.models import User
from accounts.serializers import UserRegisterSerializer, LoginSerializer, UserLightSerializer, CheckUserSerializer, \
    RestoreSerializer


class UserViewSet(GenericViewSet,CreateModelMixin):
    queryset = User.objects.all()
    serializer_class =UserRegisterSerializer

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer
        return self.serializer_class


    @action(methods=['post'],detail=False)
    def login(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        login(request, user)
        return Response({"message": "ok"})


    @action(methods=['delete'],detail=False)
    def logout(self,request):
        logout(request)
        Response({'message':'ok'})

    @action(methods=['get'],detail=False)
    def session(self,request):
        user = request.user
        serializers = UserLightSerializer(user)
        Response(data=serializers.data)





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