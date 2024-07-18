import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chess_tournament.settings")

app = Celery("chess_tournament")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
