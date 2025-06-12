import os
from celery import Celery

# Django sozlamalarini aniqlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'U2_rest.settings')

# Celery ilovasi
app = Celery('U2_rest')

# Django settings.py dan CELERY_ bilan boshlanuvchi parametrlarni olish
app.config_from_object('django.conf:settings', namespace='CELERY')

# Avto tasklarni topish
app.autodiscover_tasks()
