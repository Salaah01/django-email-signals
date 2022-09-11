"""Dynamically creates signals for registered models."""

from functools import partial
from django.db.models import signals, Model
from .constraint_checker import ConstraintChecker
from . import models, emailer


def signal_callback(
    instance: Model, signal: signals.ModelSignal, **kwargs
) -> None:
    """Callback triggered by signals. This function will check if for a given
    model instance, certain constraints are met. If so, it will send an email.
    """

    model_signals = models.Signal.get_for_model_and_signal(instance, signal)
    for model_signal in model_signals:
        if not model_signal.active:
            continue
        constraints = model_signal.constraints.all()
        if not ConstraintChecker(instance, constraints, kwargs).run_tests():
            continue

        # When the program reaches this point, the constraint checker has
        # passed.
        emailer.send_mail(
            subject=model_signal.subject,
            plain_message=model_signal.plain_message,
            html_message=model_signal.html_message,
            from_email=model_signal.from_email,
            recipient_list=instance.email_signal_recipients(
                model_signal.mailing_list
            ),
            template=model_signal.template,
            context={"instance": instance, "signal_kwargs": kwargs},
        )


def setup():
    """Dynamically connections functions to signals for each model in the
    registry.
    """

    # Import needs to happen here for unit testing - otherwise the
    # changes `registered_models` to are not picked up by the tests.
    from .registry import registered_models

    # TODO: Add support for custom signals.

    signal_types = (
        signals.pre_save,
        signals.post_save,
        signals.pre_delete,
        signals.post_delete,
    )

    signal_factory = []

    for model in registered_models.values():
        for signal_type in signal_types:
            signal_factory.append(
                partial(signal_type.connect, signal_callback, sender=model)
            )

    for function in signal_factory:
        function()
