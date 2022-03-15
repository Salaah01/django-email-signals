from django import template
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


register = template.Library()


@register.simple_tag
def model_attrs_url():
    """Returns a URL for the model attrs view if it exists."""
    try:
        return reverse("django_signals_model_attrs", args=[1]).replace(
            "1", "<content_type_id>"
        )
    except NoReverseMatch:
        return ""
