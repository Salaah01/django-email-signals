from django.apps import AppConfig, apps


class EmailSignalsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "email_signals"
    verbose_name = "Email Signals"

    def ready(self):
        """Find models which should be registered by this app and register
        them.
        """
        from .registry import add_to_registry

        for model in apps.get_models():
            if getattr(model, "EMAIL_SIGNAL_MODEL", False):
                add_to_registry(model)

        # Order matters! We need to register models before we can import
        # `signals` models as it depends on registered models.
        from . import signals

        signals.setup()
