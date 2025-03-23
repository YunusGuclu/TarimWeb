# TarımUygulama/Tarım/apps.py
from django.apps import AppConfig

class TarimConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Tarım'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()  # Scheduler'ı başlatıyoruz
        import Tarım.signals