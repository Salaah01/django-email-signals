from django.apps import AppConfig, apps


class EmailSignalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'email_signals'

    def ready(self):
        """Find models which should be registered by this app and register
        them.
        """
        from .registry import add_to_registry
        for model in apps.get_models():
            if getattr(model, 'EMAIL_SIGNAL_MODEL', False):
                add_to_registry(model)

        from . import signals  # noqa: F401