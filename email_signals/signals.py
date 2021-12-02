"""Dynamically creates signals for registered models."""

from functools import partial
from django.db.models import signals, Model
from django.core.mail import send_mail
from .registry import registered_models
from .constraint_checker import ConstraintChecker
from . import models


def signal_callback(
    instance: Model,
    signal: signals.ModelSignal,
    **kwargs
) -> None:
    """Callback triggered by signals. This function will check if for a given
    model instance, certain constraints are met. If so, it will send an email.
    """
    model_signals = models.Signal.get_for_model_and_signal(instance, signal)
    for model_signal in model_signals:
        if not ConstraintChecker(instance, kwargs).run_tests():
            continue

        # When the program reaches this point, the constraint checker has
        # passed.
        send_mail(
            subject=model_signal.subject,
            message=model_signal.plain_text_email,
            html_message=model_signal.html_email,
            from_email=model_signal.from_email,
            recipient_list=instance.email_signal_recipients(
                model_signal.to_emails_opt
            ),
        )


# The types of signals supported.
# TODO: Add support for custom signals.
signal_types = (
    signals.pre_save,
    signals.post_save,
    signals.pre_delete,
    signals.post_delete
)


# Create signals for each registered model.
signal_factory = []

for model in registered_models.values():
    for signal_type in signal_types:
        signal_factory.append(partial(
            signal_type.connect,
            signal_callback,
            sender=model
        ))

for function in signal_factory:
    function()
