from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name'
        )


class UserCreateSerializers(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validated_data(self):
        pass

    def validate_password(self, value):
        if len(value) <= 4:
            raise ValidationError({"password": "4 katta bolsin"})
        return value

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise ValidationError({"email": "Already have this email!"})
        return value
    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise ValidationError({"username": "Already have this username!"})
        return value



