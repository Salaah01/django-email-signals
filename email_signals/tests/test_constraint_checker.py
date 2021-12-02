from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from ..models import Signal, SignalConstraint
from .testcase import EmailSignalTestCase
from email_signals.constraint_checker import ConstraintChecker


class TestConstraintChecker(EmailSignalTestCase):
    """Unittests for the `ConstraintChecker` class."""

    def test_init_no_constraints(self):
        """Test the `__init__` method where there are no constraints for a
        signal.
        """
        self.create_signal(self.customer_rec)
        constraint_checker = ConstraintChecker(self.customer_rec, {})
        self.assertEqual(list(constraint_checker.constraints), [])

    def test_init_with_constraints(self):
        """Test the `__init__` method where there are constraints for a
        signal.
        """
        signal_rec = self.create_signal(self.customer_rec)
        signal_constraint = SignalConstraint.objects.create(
            signal=signal_rec,
            param_1='a',
            comparision='eq',
            param_2='b',
        )
        signal_constraint.save()
        constraint_checker = ConstraintChecker(self.customer_rec, {})

        self.assertEqual(
            list(constraint_checker.constraints),
            [signal_constraint]
        )

    
