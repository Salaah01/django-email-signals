from django.test import TestCase
from ..models import Signal
from .. import registry


class TestRegistry(TestCase):
    """Tests the functions in the registry module."""

    def setUp(self):
        # Flush the registry
        registry.registered_models = {}

    def test_model_str(self):
        """Tests the model_str function."""
        self.assertEqual(registry.model_str(Signal), 'email_signals.signal')

    def test_add_to_registry(self):
        """Tests the add_to_registry function."""
        registry.add_to_registry(Signal)
        self.assertEqual(
            list(registry.registered_models.values()),
            [Signal]
        )

    def test_model_in_registry(self):
        """Tests the model_in_registry function."""
        self.assertFalse(registry.model_in_registry(Signal))
        registry.add_to_registry(Signal)
        self.assertTrue(registry.model_in_registry(Signal))
