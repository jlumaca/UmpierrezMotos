from django.apps import AppConfig


class AppumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppUM'

    def ready(self):
        from .scheduler import iniciar_scheduler
        iniciar_scheduler()
