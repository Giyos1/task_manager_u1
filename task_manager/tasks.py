import pandas as pd
from celery import shared_task
from task_manager.models import Task


@shared_task
def export_model_to_exel():
    task = Task.objects.all().values()

    df = pd.DataFrame(list(task))
    file_path = 'media/exports/task_export.xlsx'
    df.to_excel(file_path,index=False)

    return file_path
