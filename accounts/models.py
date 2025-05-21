from django.contrib.auth import models
from django.contrib.auth.models import AbstractUser
from task_manager.models.task import Roles


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=Roles, default=Roles.MEMBER)
