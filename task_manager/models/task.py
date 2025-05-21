from django.db import models
from accounts.models import User
from task_manager.models.project import Project

class Roles(models.TextChoices):
    ADMINISTRATOR = "administrator", "Administrator"
    MEMBER = "member", "Member"
    VIEWER = "viewer", "Viewer"
    PRODUCT_OWNER = "product_owner", "Product Owner"

class TaskStatus(models.TextChoices):
    TO_DO = "to_do", "To Do"
    IN_PROGRESS = "in_progress", "In Progress"
    IN_REVIEW = "in_review", "In Review"
    DONE = "done", "Done"

# class User(AbstractUser):
#     role = models.CharField(max_length=20, choices=Roles, default=Roles.MEMBER)

    # def __str__(self):
    #     return self.username

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.TO_DO)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

























