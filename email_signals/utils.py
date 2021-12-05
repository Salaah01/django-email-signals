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

        if param_part in ('self', 'instance'):
            return True, current_object

        return False, None

    return True, current_object


def get_all_obj_attr_names(obj: _t.Any, seen_objects=None) -> dict:
    """Recursively, get all the attribute names from a object. The first object
    is expected to be a model instance.

    Args:
        obj: The object to get the attribute names from.
        seen_objects: A set of objects IDs that have already been seen.

    Returns:
        dict: The attribute names of the object.
    """
    attr_names = {}
    seen_objects = seen_objects or set()
    for attr_name in dir(obj):
        if attr_name.startswith('_'):
            continue
        attr = getattr(obj, attr_name)

        # A level of safety to prevent infinite recursion.
        if id(attr) in seen_objects:
            continue
        seen_objects.add(id(attr))

        # We don't call functions for the user to prevent security risks.
        # For that reason, we won't get the attribute names of functions.
        if callable(attr):
            continue
        attr_names[attr_name] = {}

        # If the attribute is a foreign key, get the attribute names of the
        # related object.
        if hasattr(attr, 'field') and attr.field.is_relation:
            related_model = attr.field.related_model
            if related_model != attr.field.model:
                attr_names[attr_name] = get_all_obj_attr_names(
                    related_model,
                    seen_objects
                )

    return attr_names
