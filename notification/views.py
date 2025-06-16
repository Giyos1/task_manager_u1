from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notification.models import Notification
from notification.serializers import NotificationSerializer, EmptySerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self,):
        return self.queryset.filter(user=self.request.user,is_read=False)


    @action(methods=['get'],detail=False)
    def notification_count(self,request):
        return Response({'count':self.get_queryset().count()})

    @action(methods=['get'], detail=False,serializer_class=EmptySerializer)
    def all_marked_read(self, request):
        Notification.objects.all().update(is_read=True)
        return Response({'count': self.get_queryset().count()})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer =self.get_serializer(instance)
        instance.is_read = True
        serializer.save()
        return Response(serializer.data)
