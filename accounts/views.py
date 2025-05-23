from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError

from accounts.models import User
from accounts.serializers import UserCreateSerializers


# Create your views here.

class UserCreateGenericViewSet(GenericViewSet, CreateModelMixin):
    model = User
    serializer_class = UserCreateSerializers

    def create(self, request, *args, **kwargs):
        password = request.data.get('password')
        email = request.data.get('email')
        username = request.data.get('username')
        if len(password) <= 4:
            raise ValidationError({"password": "4 katta bolsin"})
        password = make_password(password)
        data = {
            "email": email,
            "password": password,
            "username": username,
        }
        serializer = UserCreateSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        User.objects.create(**data)
        return Response({"message": "Good job!"}, status=201)
