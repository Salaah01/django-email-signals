"""Contains utility functions for the email_signals package."""

import typing as _t
from django.template import loader
from django.db.models.base import ModelBase
from django.db.models.fields.related_descriptors import ManyToManyDescriptor


def convert_to_primitive(param: str) -> _t.Any:
    """Converts the `param` to a primitive type is possible.

    Returns:
        bool: True if the `param` was converted to a primitive type.
        _t.Any: The converted value.
    """
    if param.lower() == "true":
        return True
    if param.lower() == "false":
        return False
    if param.lower() in ("none", "null"):
        return None
    if "." in param:
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
    param: str, searchable: object, seperator: str = "."
) -> (bool, _t.Any):
    """Search for the `param` in the `searchable` object. Iteratively
    search through the object's attributes until the `param` is found.

    Note: Though technically possible, this function will not call a function
    if a function is found. There is no knowing what side effects could occur
    by calling a function this way as well as any security risks associated
    with it.

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
        # supported for dictionaries in python 3.8 and below.
        if isinstance(current_object, dict):
            if param_part in current_object:
                current_object = current_object[param_part]
                continue
            else:
                return False, None

        try:
            if hasattr(current_object, param_part):
                current_object = getattr(current_object, param_part)

                # If the current object is a field, then at this point, the
                # current object may be a relation descriptor. If this is the
                # case, we need to We point the current object to the related
                # model.
                if (
                    hasattr(current_object, "field")
                    and current_object.field.is_relation
                ):
                    current_object = current_object.field.related_model
                continue
        except Exception:
            return False, None

        # Test if the current object can be converted into a number.
        if param_part.isdigit():
            try:
                iter_object = list(iter(current_object))
                if len(iter_object) > int(param_part):
                    current_object = iter_object[int(param_part)]
                    continue
            except TypeError:
                return False, None

        if param_part in ("self", "instance"):
            return True, current_object

        return False, None

    return True, current_object


def get_model_attr_names(model_class: ModelBase, seen_attrs=None) -> dict:
    """Recursively, get all the attribute names from a model class.

    Note: This function will not traverse into the `ManyToManyDescriptor`. As
    we keep a set of seen attributes, by traversing into the
    `ManyToManyDescriptor` we end up adding an attribute inside a deeper level
    of the model class which should be in a higher level.

    Args:
        model_class: The model class to get the attribute names from.
        seen_attrs: A set of objects IDs that have already been seen.

    Returns:
        dict: The attribute names of the model attributes and their subsequent
            children names.
    """
    attr_names = {}
    seen_attrs = seen_attrs or set()
    for attr_name in dir(model_class):

        # Skip private attributes.
        if attr_name.startswith("_"):
            continue

        attr = getattr(model_class, attr_name)

        # A level of safety to prevent infinite recursion.
        if id(attr) in seen_attrs:
            continue
        seen_attrs.add(id(attr))

        # We don't call functions for the user to prevent security risks.
        # For that reason, we won't get the attribute names of functions.
        if callable(attr):
            continue
        attr_names[attr_name] = {}

        # If the attribute is a foreign key, get the attribute names of the
        # related object.
        if (
            hasattr(attr, "field")
            and attr.field.is_relation
            and not isinstance(attr, ManyToManyDescriptor)
        ):
            related_model = attr.field.related_model
            if related_model != attr.field.model:
                attr_names[attr_name] = get_model_attr_names(
                    related_model, seen_attrs
                )

    return attr_names


def add_context_to_string(template_str: str, context: dict) -> str:
    """Add the context to the template string.

    Args:
        template_str: The template string to add the context to.
        context: The context to add to the template string.

    Returns:
        str: The template string with the context added.
    """
    engines = loader._engine_list()
    for engine in engines:
        try:
            template = engine.from_string(template_str)
            return template.render(context)
        except AttributeError:
            continue
    else:
        raise ValueError(
            "Could not find a template engine that can render the string."
        )
