import pandas as pd
from celery import shared_task
from notification.models import Notification
from task_manager.models import Task


@shared_task
def export_model_to_exel():
    task = Task.objects.all().values()

    df = pd.DataFrame(list(task))
    file_path = 'media/exports/task_export.xlsx'
    df.to_excel(file_path,index=False)

    return file_path


@shared_task
def notification_for_task(user,message):
    Notification.objects.create(
        title = "You've been given a task.",
        message = message,
        user = user
    )
    print()



@shared_task
def notification_update_status(user,message):
    print("notification creating")
    notification=Notification.objects.create(
        title = "Task complated",
        message = message,
        user = user
    )
    print(f"Notification{notification}")