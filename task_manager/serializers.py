from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from task_manager.models.task import User, Task, TaskStatus
from task_manager.models.project import Project

class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'role')
        read_only_fields = ('id',)

class ProjectLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)

class ProjectListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    product_owner = UserLightSerializer(read_only=True)
    project_members = UserLightSerializer(many=True, read_only=True)

class ProjectCreateAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'product_owner', 'project_members')
        read_only_fields = ('id',)
        extra_kwargs = {
            'project_members': {'write_only': True},
        }

    def validate_name(self, value):
        if len(value) <= 3:
            raise ValidationError('3 ta harfdan katta bo‘lsin')
        instance_id = getattr(self.instance, 'id', None)
        if Project.objects.filter(name=value).exclude(id=instance_id).exists():
            raise ValidationError('Bunday nomli loyiha mavjud')
        return value

    def validate(self, attrs):
        if attrs.get('description') == attrs.get('name'):
            raise ValidationError({"description_name": 'name va description bir xil bo‘lmasligi kerak'})
        return attrs

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.product_owner = validated_data.get('product_owner', instance.product_owner)
        instance.save()
        return instance

class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'product_owner', 'project_members')
        read_only_fields = ('id', 'project_members')

class TaskListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True)
    status = serializers.ChoiceField(choices=TaskStatus.choices)
    assigned_to = UserLightSerializer(read_only=True)
    reviewer = UserLightSerializer(read_only=True)
    project = ProjectLightSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

class TaskCreateAndUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'assigned_to', 'reviewer', 'project', 'created_at')
        read_only_fields = ('id', 'created_at')
        extra_kwargs = {
            'assigned_to': {'write_only': True},
            'reviewer': {'write_only': True},
        }

    def validate_title(self, value):
        if len(value) <= 3:
            raise ValidationError('3 ta harfdan katta bo‘lsin')
        return value