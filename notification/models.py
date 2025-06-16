from django.db import models
from accounts.models import User


class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notification')
    title = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)


