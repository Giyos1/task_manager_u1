from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserLightSerializer
from task_manager.models import Project, Task


class TaskLightSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()

    class Meta:
        model = Task
        fields = 'id', 'title', 'status', 'user',


class TaskCreateSerializers(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=7)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = 'title', 'project', 'status', 'user'


class TaskPatchStatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=7)
