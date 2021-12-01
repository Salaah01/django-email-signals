"""Dynamically creates signals for registered models."""

from functools import partial
from django.db.models import signals, Model
from .registry import registered_models

signal_factory = []


def signal_callback(**kwargs) -> None:
    print(f"{kwargs['sender'].__name__} was saved")


signal_types = (
    signals.pre_save,
    signals.post_save,
    signals.pre_delete,
    signals.post_delete
)

for model in registered_models.values():
    for signal_type in signal_types:
        signal_factory.append(partial(
            signal_type.connect,
            signal_callback,
            sender=model
        ))

for function in signal_factory:
    function()
