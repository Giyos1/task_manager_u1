from django.db.models import CharField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.serializers import UserLightSerializer
from task_manager.models import Project, Task


# from task_manager.models import Project
def validate_name(value):
    if len(value) <= 3:
        raise ValidationError('3 ta harfdan katta bolsin')
    return value


class ProjectListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, validators=[validate_name])
    description = serializers.CharField()
    owner = UserLightSerializer()


class ProjectCreateAndUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'owner'
        )

    def validate_name(self, value):

        if len(value) <= 3:
            raise ValidationError('3 ta harfdan katta bolsin')
        return value

    def validate(self, attrs):
        description = attrs.get('description')
        name = attrs.get("name")

        if description == name:
            raise ValidationError({"description_name": 'name va description hbir xil bolmasligi kerak'})

        return attrs


class ProjectDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'owner'
        )


class ProjectLightSerializers(serializers.ModelSerializer):
    owner = UserLightSerializer

    class Meta:
        model = Project
        fields = 'name', 'description', 'owner'


class TaskLightSerializer(serializers.ModelSerializer):
    user = UserLightSerializer
    project = ProjectLightSerializers

    class Meta:
        model = Task
        fields = 'title', 'status', 'project', 'user',
