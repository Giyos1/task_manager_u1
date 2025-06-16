from rest_framework import serializers
from notification.models import Notification


class EmptySerializer(serializers.Serializer):
    pass

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'title',
            'is_read',
            'message'
        ]
