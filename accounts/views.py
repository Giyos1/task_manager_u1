from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from accounts.serializers import UserCreateSerializers


# Create your views here.

class UserCreateGenericViewSet(GenericViewSet, CreateModelMixin):
    model = User
    serializer_class = UserCreateSerializers

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**request.data)
        return Response({"message": "Good job!"}, status=201)
