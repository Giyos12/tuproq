from django.apps import AppConfig


class UathConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uath'

    def ready(self):
        import uath.signals
