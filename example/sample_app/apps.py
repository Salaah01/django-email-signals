from django.apps import AppConfig


class SampleAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sample_app'

    def ready(self):
        from . import signals  # noqa: F401