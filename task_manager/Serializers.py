from symtable import Class

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.models import User
from accounts.serializers import UserLightSerializer
from task_manager.models import Project, Task



# from task_manager.models import Project
def validate_name(value):
    if len(value) <= 3:
        raise ValidationError('3 ta harfdan katta bolsin')
    return value




class ProjectLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id'
            'name',
            'description',
            'owner',
            'members'
        )

        read_only_field =['id','owner','members']




class TaskListSerializer(serializers.ModelSerializer):

   project = ProjectLightSerializer(read_only=True,many=True)
   user = UserLightSerializer(read_only=True,many=True)

   class Meta:
        model = Task
        field = (
        'id',
        'title',
        'project',
        'user',
        'status'
        )

   read_only_fields =['id',],


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'project',
            'user',
            'status'

        )

    read_only_fields = ['id', 'project', 'user']


class TaskCreateAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'project',
            'user',
            'status'
        ]

    def validate_title(self, value, ):
        if not value.isalpha():
            raise ValidationError('Malumotni matn korinishida kiritihsingiz kerak')


class ProjectListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, validators=[validate_name])
    description = serializers.CharField()
    owner = UserLightSerializer()
    tasks =TaskListSerializer(read_only=True,many=True)


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



