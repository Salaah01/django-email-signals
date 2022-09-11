import typing as _t
from django.db.models import Model
from .models import SignalConstraint
from . import constraint_methods, utils


class ConstraintChecker:
    """Determines whether a model instance satisfies a constraints and
    determines if it is able to raise a signal.
    """

    def __init__(
        self, instance: Model, constraints: _t.List[Model], signal_kwargs: dict
    ):
        """Initialise the checker with the instance and signal kwargs.

        Args:
            instance: The model instance on which a signal is to be raised.
            constraints: The constraints for the model instance
            signal_kwargs: The kwargs retrieved from the signal handler.
        """
        self.instance = instance
        self.signal_kwargs = signal_kwargs
        self.constraints = constraints

    def run_tests(self) -> bool:
        """Run all tests and return `True` if all tests pass."""
        for constraint in self.constraints:
            p1, p2 = self.get_params(constraint)
            if not self.check_constraint(p1, p2, constraint.comparison):
                return False
        return True

    def get_params(
        self, constraint: SignalConstraint
    ) -> _t.Tuple[_t.Any, _t.Any]:
        """Given a `constraint` param fields, retrieve actual values.

        Args:
            constraint: The constraint to retrieve the params for.

        Returns:
            A tuple of the actual values of the params.
        """

        return (
            self.get_param_1(constraint.param_1),
            self.get_param_2(constraint.param_2),
        )

    def get_param_1(self, param_1: str) -> _t.Any:
        """Given `param_1` from the constraints, retrieve it's actual value.

        Args:
            param_1: The param_1 field from the constraint.

        Returns:
            The actual value of the param_1 field.
        """
        if not param_1:
            raise ValueError("`param_1` is a required field.")

        success, param_1_val = utils.get_param_from_obj(
            param_1, self.signal_kwargs
        )
        if success:
            return param_1_val

        success, param_1_val = utils.get_param_from_obj(param_1, self.instance)
        if not success:
            raise ValueError(
                f"ContainsChecker: param_1 {param_1} not found in kwargs "
                "nor in model instance"
            )
        return param_1_val

    def get_param_2(self, param_2: str) -> _t.Any:
        """Given `param_2` from the constraints, retrieve it's actual value.

        Args:
            param_2: The param_2 field from the constraint.

        Returns:
            The actual value of the param_2 field.
        """
        if param_2 is None:
            return None

        success, param_2_val = utils.get_param_from_obj(
            param_2, self.signal_kwargs
        )
        if success:
            return param_2_val

        success, param_2_val = utils.get_param_from_obj(param_2, self.instance)
        if success:
            return param_2_val

        return utils.convert_to_primitive(param_2)

    @staticmethod
    def check_constraint(
        param_1: _t.Any, param_2: _t.Any, comparison: str
    ) -> bool:
        """Check if `param_1` and `param_2` satisfy the constraint.

        Args:
            param_1: First parameter to check.
            param_2: Second parameter to check.
            comparison: Comparison method to use.

        Returns:
            True if `param_1` and `param_2` satisfy the constraint.
        """

        method = getattr(constraint_methods, comparison, None)
        if method is None:
            raise ValueError(
                f"ContainsChecker: comparison {comparison} not found in "
                "constraint_methods"
            )
        return method(param_1, param_2)


def comparison_requires_2_params(comparison: str) -> bool:
    """Check if the comparison requires 2 params.

    Args:
        comparison: The comparison to check.

    Returns:
        True if the comparison requires 2 params.
    """
    return comparison in [
        "exact",
        "iexact",
        "contains",
        "icontains",
        "gt",
        "gte",
        "lt",
        "lte",
        "startswith",
        "istartswith",
        "endswith",
        "iendswith",
        "regex",
        "iregex",
    ]
