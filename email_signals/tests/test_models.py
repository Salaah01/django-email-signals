from django.db.models import signals
from .testcase import EmailSignalTestCase
from .. import models


class TestEmailSignalMixin(EmailSignalTestCase):
    """Unittests for the `EmaiLSignalMixin`."""

    def test_email_signal_recipients(self):
        """Test the `email_signal_recipients` method."""

        self.assertIsInstance(
            self.customer_rec.email_signal_recipients("my_mailing_list"), list
        )

    def test_email_signal_emails_recipients(self):
        """Test the `email_signal_recipients` method with provided emails."""

        self.assertIsInstance(
            self.customer_rec.email_signal_recipients(
                "test@email.com,test1@email.com"
            ),
            list,
        )

    def test_email_signal_recipients_invalid(self):
        """Test the `email_signal_recipients` method with an invalid function
        name. It should raise an `NotImplementedError`.
        """

        with self.assertRaises(NotImplementedError):
            self.customer_rec.email_signal_recipients("invalid_function")


class TestSignal(EmailSignalTestCase):
    """Unittests for the `Signal` model."""

    def test_str(self):
        """Test the `__str__` method."""
        self.assertIsInstance(str(self.create_signal(self.customer_rec)), str)

    def test_get_signal_type(self):
        """Test the `get_signal_type` method."""
        self.assertIsInstance(
            self.create_signal(self.customer_rec).get_signal_type(),
            signals.ModelSignal,
        )

    def test_get_choice_from_signal(self):
        """Test the `get_choice_from_signal` method returns the correct
        signal type choice.
        """
        choices = models.Signal.SignalTypeChoices
        self.assertEqual(
            models.Signal.get_choice_from_signal(signals.pre_save),
            choices.pre_save,
        )
        self.assertEqual(
            models.Signal.get_choice_from_signal(signals.post_save),
            choices.post_save,
        )
        self.assertEqual(
            models.Signal.get_choice_from_signal(signals.pre_delete),
            choices.pre_delete,
        )
        self.assertEqual(
            models.Signal.get_choice_from_signal(signals.post_delete),
            choices.post_delete,
        )

    def test_get_choice_from_signal_invalid(self):
        """Test the `get_choice_from_signal` method with an invalid signal
        type. It should raise an `ValueError`.
        """
        with self.assertRaises(ValueError):
            models.Signal.get_choice_from_signal("invalid_signal")

    def test_get_for_model_and_signal(self):
        """Test the `get_for_model_and_signal` method. Given the model and
        signal, it should return a queryset of `Signal`.
        """
        qs = models.Signal.get_for_model_and_signal(
            self.customer_rec, signals.pre_save
        )

        for q in qs:
            self.assertEqual(q.model, self.customer_rec)
            self.assertEqual(q.signal, signals.pre_save)

    def test_constraints_count(self):
        """Test the `constraints_count` property. It should return the number
        of constraints.
        """
        signal = self.create_signal(self.customer_rec)
        self.assertEqual(signal.constraints_count, 0)

        models.SignalConstraint.objects.create(
            signal=signal, param_1="self", comparison="istrue"
        ).save()
        models.SignalConstraint.objects.create(
            signal=signal, param_1="self", comparison="gt", param_2=10
        ).save()

        self.assertEqual(signal.constraints_count, 2)

    def test_model(self):
        """Test the `model` property."""
        self.assertEqual(
            self.create_signal(self.customer_rec).model,
            self.customer_rec.__class__,
        )

    def test_is_pre_save(self):
        """Test the `is_pre_save` property."""
        signal = self.create_signal(self.customer_rec)
        self.assertTrue(signal.is_pre_save())
        signal.signal_type = models.Signal.SignalTypeChoices.post_save
        self.assertFalse(signal.is_pre_save())

    def test_is_post_save(self):
        """Test the `is_post_save` property."""
        signal = self.create_signal(self.customer_rec)
        self.assertFalse(signal.is_post_save())
        signal.signal_type = models.Signal.SignalTypeChoices.post_save
        self.assertTrue(signal.is_post_save())

    def test_is_pre_delete(self):
        """Test the `is_pre_delete` property."""
        signal = self.create_signal(self.customer_rec)
        self.assertFalse(signal.is_pre_delete())
        signal.signal_type = models.Signal.SignalTypeChoices.pre_delete
        self.assertTrue(signal.is_pre_delete())

    def test_is_post_delete(self):
        """Test the `is_post_delete` property."""
        signal = self.create_signal(self.customer_rec)
        self.assertFalse(signal.is_post_delete())
        signal.signal_type = models.Signal.SignalTypeChoices.post_delete
        self.assertTrue(signal.is_post_delete())


class TestSignalConstraint(EmailSignalTestCase):
    """Unittests for the `SignalConstraint` model."""

    def test_str(self):
        signal = self.create_signal(self.customer_rec)
        signal_constraint = models.SignalConstraint.objects.create(
            signal=signal, param_1="self", comparison="istrue"
        )
        self.assertIsInstance(str(signal_constraint), str)
