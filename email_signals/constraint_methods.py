import typing as _t
import re


def exact(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if two objects are equal."""
    return param_1 == param_2


def iexact(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if two objects are equal, ignoring case."""
    if isinstance(param_1, str) and isinstance(param_2, str):
        return param_1.lower() == param_2.lower()
    return exact(param_1, param_2)


def contains(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 contains param_2."""
    if isinstance(param_1, str) and isinstance(param_2, str):
        return param_2 in param_1
    return False


def icontains(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 contains param_2, ignoring case."""
    if isinstance(param_1, str) and isinstance(param_2, str):
        return param_2.lower() in param_1.lower()
    return False


def gt(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 is greater than param_2."""
    try:
        return float(param_1) > float(param_2)
    except (TypeError, ValueError):
        return False


def gte(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 is greater than or equal to param_2."""
    try:
        return float(param_1) >= float(param_2)
    except (TypeError, ValueError):
        return False


def lt(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 is less than param_2."""
    try:
        return float(param_1) < float(param_2)
    except (TypeError, ValueError):
        return False


def lte(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 is less than or equal to param_2."""
    try:
        return float(param_1) <= float(param_2)
    except (TypeError, ValueError):
        return False


def startswith(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 starts with param_2."""
    if isinstance(param_1, str) and isinstance(param_2, str):
        return param_1.startswith(param_2)
    return False


def istartswith(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 starts with param_2, ignoring case."""
    if isinstance(param_1, str) and isinstance(param_2, str):
        return param_1.lower().startswith(param_2.lower())
    return False


def endswith(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 ends with param_2."""
    if isinstance(param_1, str) and isinstance(param_2, str):
        return param_1.endswith(param_2)
    return False


def iendswith(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 ends with param_2, ignoring case."""
    if isinstance(param_1, str) and isinstance(param_2, str):
        return param_1.lower().endswith(param_2.lower())
    return False


def regex(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 matches param_2."""
    if isinstance(param_1, str) and isinstance(param_2, str):
        return re.match(param_2, param_1) is not None
    return False


def iregex(param_1: _t.Any, param_2: _t.Any) -> bool:
    """Check if param_1 matches param_2, ignoring case."""
    if isinstance(param_1, str) and isinstance(param_2, str):
        return re.match(param_2, param_1, re.IGNORECASE) is not None
    return False


def isnull(param_1: _t.Any, _=None) -> bool:
    """Check if param_1 is null."""
    return param_1 is None


def isnotnull(param_1: _t.Any, _=None) -> bool:
    """Check if param_1 is not null."""
    return param_1 is not None


def istrue(param_1: _t.Any, _=None) -> bool:
    """Check that param_1 is truthy."""
    return bool(param_1)


def isfalse(param_1: _t.Any, _=None) -> bool:
    """Check that param_1 is falsy."""
    return not bool(param_1)
