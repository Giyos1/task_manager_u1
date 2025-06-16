from django.template.defaultfilters import title

from task_manager.models import Task
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from task_manager.tasks import notification_for_task, notification_update_status


@receiver(post_save,sender=Task)
def send_task_notification(sender,instance,created,**kwargs):
    if created:
        user = instance.user.id
        message = f"New task {instance.title}"
        notification_for_task.delay(user,message)



@receiver(pre_save, sender=Task)
def update_task_status(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    if old_instance.status != 'Done' and instance.status == 'Done':
        user = instance.user.id
        message = f'Your task {instance.title} has been marked as completed'
        notification_update_status.delay(user, message)
