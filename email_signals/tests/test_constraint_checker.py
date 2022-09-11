from ..models import SignalConstraint
from .testcase import EmailSignalTestCase
from email_signals.constraint_checker import (
    ConstraintChecker,
    comparison_requires_2_params,
)


class TestConstraintChecker(EmailSignalTestCase):
    """Unittests for the `ConstraintChecker` class."""

    def test_init_no_constraints(self):
        """Test the `__init__` method where there are no constraints for a
        signal.
        """
        self.create_signal(self.customer_rec)
        constraint_checker = ConstraintChecker(self.customer_rec, [], {})
        self.assertEqual(list(constraint_checker.constraints), [])

    def test_init_with_constraints(self):
        """Test the `__init__` method where there are constraints for a
        signal.
        """
        signal_rec = self.create_signal(self.customer_rec)
        signal_constraint = SignalConstraint.objects.create(
            signal=signal_rec,
            param_1="a",
            comparison="eq",
            param_2="b",
        )
        signal_constraint.save()
        constraints = signal_rec.constraints.all()
        constraint_checker = ConstraintChecker(
            self.customer_rec, constraints, {}
        )

        self.assertEqual(
            list(constraint_checker.constraints), [signal_constraint]
        )

    def test_check_constraint(self):
        """Test the `check_constraint` method."""
        self.assertTrue(ConstraintChecker.check_constraint("a", "a", "exact"))
        self.assertFalse(ConstraintChecker.check_constraint("a", "b", "exact"))

    def test_check_constraint_invalid_comparison(self):
        """Test the `check_constraint` method with an invalid comparison."""
        with self.assertRaises(ValueError):
            ConstraintChecker.check_constraint("a", "b", "abc")

    def test_get_params_bad_param_1(self):
        """Test the `get_param_1` method where the `param_1` is invalid. This
        should raise a `ValueError` as `param_1` is expected to exist in
        some level of the model instance or the signal kwargs.
        """
        signal = self.create_signal(self.customer_rec)
        constraint = SignalConstraint.objects.create(
            signal=signal,
            param_1="zzz",
            comparison="eq",
            param_2="b",
        )
        constraint.save()
        constraints = signal.constraints.all()
        constaint_checker = ConstraintChecker(
            self.customer_rec, constraints, {}
        )

        with self.assertRaises(ValueError):
            constaint_checker.get_param_1(constraint.param_1)

    def test_get_param_1_in_kwargs(self):
        """Test the `get_param_1` method where the `param_1` is in the
        signal kwargs.
        """
        signal = self.create_signal(self.customer_rec)
        constraint = SignalConstraint.objects.create(
            signal=signal,
            param_1="a.b",
            comparison="eq",
            param_2=None,
        )
        constraint.save()
        constraints = signal.constraints.all()
        constaint_checker = ConstraintChecker(
            self.customer_rec, constraints, {"a": {"b": 1}}
        )

        self.assertEqual(constaint_checker.get_param_1(constraint.param_1), 1)

    def test_get_param_1_in_instance(self):
        """Test the `get_param_1` method where the `param_1` is in the
        model instance.
        """
        self.customer_rec.name = "Test Name"
        self.customer_rec.save()

        signal = self.create_signal(self.customer_order_rec)
        constraint = SignalConstraint.objects.create(
            signal=signal,
            param_1="customer.name",
            comparison="eq",
            param_2=None,
        )
        constraint.save()
        constraints = signal.constraints.all()
        constaint_checker = ConstraintChecker(
            self.customer_order_rec, constraints, {}
        )

        self.assertEqual(
            constaint_checker.get_param_1(constraint.param_1), "Test Name"
        )

    def test_get_param_2_in_kwargs(self):
        """Test the `get_param_2` method where the `param_2` is in the
        signal kwargs.
        """
        signal = self.create_signal(self.customer_rec)
        constraint = SignalConstraint.objects.create(
            signal=signal,
            param_1="a",
            comparison="eq",
            param_2="a.b",
        )
        constraint.save()
        constraints = signal.constraints.all()
        constaint_checker = ConstraintChecker(
            self.customer_rec, constraints, {"a": {"b": 1}}
        )

        self.assertEqual(constaint_checker.get_param_1(constraint.param_2), 1)

    def test_get_param_2_in_instance(self):
        """Test the `get_param_2` method where the `param_2` is in the
        model instance.
        """
        self.customer_rec.name = "Test Name"
        self.customer_rec.save()

        signal = self.create_signal(self.customer_order_rec)
        constraint = SignalConstraint.objects.create(
            signal=signal,
            param_1="a",
            comparison="eq",
            param_2="customer.name",
        )
        constraint.save()
        constraints = signal.constraints.all()
        constaint_checker = ConstraintChecker(
            self.customer_order_rec, constraints, {}
        )

        self.assertEqual(
            constaint_checker.get_param_2(constraint.param_2), "Test Name"
        )

    def test_get_param_2_in_primitive(self):
        """Test the `get_param_2` method where the `param_2` can be converted
        into a primitive value.
        """
        signal = self.create_signal(self.customer_rec)
        constraint = SignalConstraint.objects.create(
            signal=signal,
            param_1="a",
            comparison="eq",
            param_2="b",
        )
        constraint.save()
        constraints = signal.constraints.all()
        constaint_checker = ConstraintChecker(
            self.customer_rec, constraints, {}
        )

        self.assertEqual(
            constaint_checker.get_param_2(constraint.param_2), "b"
        )

    def test_get_params(self):
        """Test the `get_params` method."""
        signal = self.create_signal(self.customer_rec)
        constraint = SignalConstraint.objects.create(
            signal=signal,
            param_1="a",
            comparison="eq",
            param_2="1.1",
        )
        constraint.save()
        constraints = signal.constraints.all()
        constaint_checker = ConstraintChecker(
            self.customer_rec, constraints, {"a": 1}
        )

        self.assertEqual(constaint_checker.get_params(constraint), (1, 1.1))

    def test_run_tests_passes(self):
        """Test the `run_tests` method where the constraints should pass."""
        signal = self.create_signal(self.customer_rec)
        constraint = SignalConstraint.objects.create(
            signal=signal,
            param_1="a",
            comparison="exact",
            param_2="1.1",
        )
        constraint.save()
        constraints = signal.constraints.all()
        constaint_checker = ConstraintChecker(
            self.customer_rec, constraints, {"a": 1.1}
        )

        self.assertTrue(constaint_checker.run_tests())

    def test_run_tests_fails(self):
        """Test the `run_tests` method where the constraints should fail."""
        signal = self.create_signal(self.customer_rec)
        constraint = SignalConstraint.objects.create(
            signal=signal,
            param_1="a",
            comparison="exact",
            param_2="1.1",
        )
        constraint.save()
        constraints = signal.constraints.all()
        constaint_checker = ConstraintChecker(
            self.customer_rec, constraints, {"a": 1}
        )

        self.assertFalse(constaint_checker.run_tests())

    def test_comparison_requires_2_params(self):
        """Test the `comparison_requires_2_params` method."""
        self.assertTrue(comparison_requires_2_params("exact"))
        self.assertFalse(comparison_requires_2_params("istrue"))
