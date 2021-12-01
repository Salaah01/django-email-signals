from django.db import models
from . registry import add_to_registry


class EmailSignalMixin:
    """A mixin to add a model to the email_signals app."""

    EMAIL_SIGNAL_MODEL = True

    def email_signal_post_init(self) -> None:
        """Add this model to the registry."""
        add_to_registry(self)
