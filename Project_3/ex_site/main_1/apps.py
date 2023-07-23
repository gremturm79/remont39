from django.apps import AppConfig


class Main1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_1'

    def ready(self):
        import main_1.signals
