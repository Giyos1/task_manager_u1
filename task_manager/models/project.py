from django.db import models
from accounts.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    product_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='product_manager',)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='project_members')

    def __str__(self):
        return self.name
