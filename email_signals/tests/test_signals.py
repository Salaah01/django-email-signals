from django.core import mail
from django.db.models import signals as django_signals
from .testcase import EmailSignalTestCase
from .. import signals, models


class TestSignals(EmailSignalTestCase):
    """Test signals."""

    def test_signal_callback_with_no_constraints(self):
        """Test signal callback where there are no additional constraints
        applied to a signal.
        """
        self.create_signal(self.customer_rec)
        signals.signal_callback(self.customer_rec, django_signals.pre_save)
        self.assertEqual(len(mail.outbox), 1)

    def test_signal_callback_with_template(self):
        """Test signal callback where a template is applied to a signal."""
        self.create_signal(
            self.customer_rec,
            template="email_signals/tests/test_emailer.html",
        )
        signals.signal_callback(self.customer_rec, django_signals.pre_save)
        self.assertEqual(len(mail.outbox), 1)

    def test_signal_failing_constraints(self):
        """Test signal callback where the model instance fails the constraint
        checker. The expected outcome is that the email should not be sent.
        """
        signal = self.create_signal(
            self.customer_rec,
            template="email_signals/tests/test_emailer.html",
        )
        # This constraint will fail as it will attempt to check if
        # `instance.id` is equal to '-1'
        models.SignalConstraint.objects.create(
            signal=signal, param_1="id", param_2="-1", comparison="exact"
        )
        signals.signal_callback(self.customer_rec, django_signals.pre_save)
        self.assertEqual(len(mail.outbox), 0)

    def test_signal_passing_constraints(self):
        """Test signal callback where the model instance passes the constraint
        checker. The expected outcome is that the email should be sent.
        """
        signal = self.create_signal(
            self.customer_rec,
            template="email_signals/tests/test_emailer.html",
        )
        # This constraint will pass as it will attempt to check if
        # `instance.id` is greater than or equal to `1`
        models.SignalConstraint.objects.create(
            signal=signal, param_1="id", param_2="1", comparison="gte"
        )
        signals.signal_callback(self.customer_rec, django_signals.pre_save)
        self.assertEqual(len(mail.outbox), 1)

    def test_pre_save_signal(self):
        """Test the `pre_save` signal is triggered correctly."""
        self.setup_signals()
        self.create_signal(self.customer_rec).save()
        self.Customer.create_record()
        # Runs twice as the create record methods saves it after creation.
        self.assertEqual(len(mail.outbox), 2)

    def test_post_save_signal(self):
        """Test the `post_save` signal is triggered correctly."""
        self.setup_signals()
        self.create_signal(
            self.customer_rec,
            signal_type=models.Signal.SignalTypeChoices.post_save,
        ).save()

        self.Customer.create_record()
        # Runs twice as the create record methods saves it after creation.
        self.assertEqual(len(mail.outbox), 2)

    def test_pre_delete_signal(self):
        """Test the `pre_delete` signal is triggered correctly."""
        self.setup_signals()
        self.create_signal(
            self.customer_rec,
            signal_type=models.Signal.SignalTypeChoices.pre_delete,
        ).save()

        rec = self.Customer.create_record()
        rec.delete()
        self.assertEqual(len(mail.outbox), 1)

    def test_post_delete_signal(self):
        """Test the `post_delete` signal is triggered correctly."""
        self.setup_signals()
        self.create_signal(
            model_instance=self.customer_rec,
            signal_type=models.Signal.SignalTypeChoices.post_delete,
        ).save()

        rec = self.Customer.create_record()
        rec.delete()
        self.assertEqual(len(mail.outbox), 1)

    def test_on_created_only(self):
        """Test that the signal is only called when a record is created."""
        self.setup_signals()
        signal = self.create_signal(
            self.customer_rec,
            signal_type=models.Signal.SignalTypeChoices.post_save,
        )
        signal.save()
        models.SignalConstraint.objects.create(
            signal=signal, param_1="created", comparison="istrue"
        ).save()
        record = self.Customer.create_record()
        record.save()

        self.assertEqual(len(mail.outbox), 1)
