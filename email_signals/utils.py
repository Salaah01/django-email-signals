"""Contains utility functions for the email_signals package."""

import typing as _t


def convert_to_primitive(param: str) -> _t.Any:
    """Converts the `param` to a primitive type is possible.

    Returns:
        bool: True if the `param` was converted to a primitive type.
        _t.Any: The converted value.
    """
    if param.lower() == 'true':
        return True
    if param.lower() == 'false':
        return False
    if param.lower() in ('none', 'null'):
        return None
    if '.' in param:
        try:
            return float(param)
        except ValueError:
            pass
    try:
        return int(param)
    except ValueError:
        pass
    return param


def get_param_from_obj(
    param: str,
    searchable: object,
    seperator: str = '.'
) -> (bool, _t.Any):
    """Search for the `param` in the `searchable` object. Iteratively
    search through the object's attributes until the `param` is found.

    Note: Though technically possible, this function will not call a function
    if a function is found as this could be a security risk.

    Args:
        param: The param to get the value for.
        searchable: The object to search for the param.
        seperator: The seperator to split the param by.

    Returns:
        bool: True if the `param` was found in the `self.instance` object.
        _t.Any: The value of the `param`.
    """
    param_parts = param.split(seperator)
    current_object = searchable

    while param_parts:
        param_part = param_parts.pop(0)

        # Need to search in a dictionary separately as `hasattr` is not
        # supported for dictionaries of python 3.8 and below.
        if isinstance(current_object, dict):
            if param_part in current_object:
                current_object = current_object[param_part]
                continue
            else:
                return False, None

        try:
            if hasattr(current_object, param_part):
                current_object = getattr(current_object, param_part)
                continue
        except Exception:
            return False, None

        # Test if the current object is iterable.
        if param_part.isdigit():
            try:
                iter_object = list(iter(current_object))
                if len(iter_object) > int(param_part):
                    current_object = iter_object[int(param_part)]
                    continue
            except TypeError:
                return False, None

        return False, None

    return True, current_object
