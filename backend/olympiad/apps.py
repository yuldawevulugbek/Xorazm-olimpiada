from django.apps import AppConfig


class OlympiadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'olympiad'

    def ready(self):
        from . import signals  # noqa: F401
