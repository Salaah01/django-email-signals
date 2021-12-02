import typing as _t
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType

from .models import Signal, SignalConstraint
from . import constraint_methods


class ConstaintChecker:
    """Checks that for a model instance that has a potential signal that it can
    raise, firstly passes all the tests required for that instance to be
    permitted to raise the signal.
    """

    def __init__(self, instance: Model, signal_kwargs: dict):
        self.instance = instance
        self.signal_kwargs = signal_kwargs
        self.constraints = SignalConstraint.objects.filter(
            signal=Signal.objects.get(
                content_type=ContentType.objects.get_for_model(instance)
            )
        )

    def run_tests(self) -> bool:
        """Run all tests and return `True` if all tests pass."""
        for constraint in self.constraints:
            param_1, param_2 = self.get_params(constraint)
            if not self.check_constraint(param_1, param_2,
                                         constraint.comparision):
                return False
        return True

    def get_params(
        self,
        constraint: SignalConstraint
    ) -> _t.Tuple[_t.Any, _t.Any]:
        """Given a `constraint` param fields, retrieve actual values."""
        param_1 = constraint.param_1
        param_2 = constraint.param_2

        if param_1 in self.signal_kwargs:
            param_1_val = self.signal_kwargs[param_1]
        elif hasattr(self.instance, param_1):
            param_1_val = getattr(self.instance, param_1)
        else:
            raise ValueError(
                f"ContainsChecker: param_1 {param_1} not found in kwargs or \
                in instance"
            )

        if param_2 is None:
            param_2_val = None
        elif param_2 in self.signal_kwargs:
            param_2_val = self.signal_kwargs[param_2]
        elif hasattr(self.instance, param_2):
            param_2_val = getattr(self.instance, param_2)
        else:
            passed, param_2_val = self.convert_to_primitive(param_2)
            if not passed:
                raise ValueError(
                    f"ContainsChecker: param_2 {param_2} not found in kwargs \
                    or in instance"
                )

        return param_1_val, param_2_val

    @staticmethod
    def convert_to_primitive(param: str) -> (bool, _t.Any):
        """Converts the `param` to a primitive type is possible.

        Returns:
            bool: True if the `param` was converted to a primitive type.
            _t.Any: The converted value.
        """
        if param.lower() == 'true':
            return True, True
        if param.lower() == 'false':
            return True, False
        if param.lower() == 'none':
            return True, None
        if param.lower() == 'null':
            return True, None
        if '.' in param:
            try:
                return True, float(param)
            except ValueError:
                pass
        try:
            return True, int(param)
        except ValueError:
            pass
        return False, param

    @staticmethod
    def check_constraint(
        param_1: _t.Any,
        param_2: _t.Any,
        comparision: str
    ) -> bool:
        """Check if `param_1` and `param_2` satisfy the constraint.

        Args:
            param_1: First parameter to check.
            param_2: Second parameter to check.
            comparision: Comparison method to use.

        Returns:
            True if `param_1` and `param_2` satisfy the constraint.
        """

        method = getattr(constraint_methods, comparision, None)
        if method is None:
            raise ValueError(
                f"ContainsChecker: comparison {comparison} not found in \
                constraint_methods"
            )
        return method(param_1, param_2)
