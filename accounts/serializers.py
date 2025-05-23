from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User
from django.db import models


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name'
        )


class UserCreateSerializers(serializers.Serializer):
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


