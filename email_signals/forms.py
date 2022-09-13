from django import forms
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.utils.html import format_html
from . import models
from .registry import registered_content_types
from .utils import get_param_from_obj
from .constraint_checker import comparison_requires_2_params


def render_js(cls):
    """Forcing all media forms to be deferred."""
    return [
        format_html(
            '<script defer src="{}"></script>', cls.absolute_path(path)
        )
        for path in cls._js
    ]


forms.widgets.Media.render_js = render_js


class SignalAdminForm(forms.ModelForm):
    class Meta:
        model = models.Signal
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Limit the content type choices to the registered content types
        self.fields["content_type"].queryset = registered_content_types()

    def clean(self):
        cleaned_data = super().clean()
        if self.is_valid():
            self._clean_mailing_list()
        return cleaned_data

    def _clean_mailing_list(self):
        """The `mailing_list` field contains a string which corresponds to a
        method that should exist in the model. Check that the function does
        exists. OR The mailing list can be a list of emails, there should be at
        least one email.
        """
        mailing_list = self.cleaned_data["mailing_list"]
        content_type = self.cleaned_data["content_type"]

        if (
            not hasattr(content_type.model_class(), mailing_list)
            and "@" not in mailing_list
        ):
            raise forms.ValidationError(
                f"The model does not have a function called {mailing_list} "
                "and the mailing list does not contain a list of emails"
            )
        return mailing_list

    def clean_template(self):
        """Check that the template exists."""
        template = self.cleaned_data["template"]
        if not template:
            return template
        try:
            get_template(template)
        except TemplateDoesNotExist:
            raise forms.ValidationError(
                f"The template {template} does not exist"
            )
        return template


class SignalConstraintAdminForm(forms.ModelForm):
    class Meta:
        models = models.SignalConstraint
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set autocomplete off for all fields.
        for field in self.fields:
            self.fields[field].widget.attrs["autocomplete"] = "off"

    def clean(self):
        cleaned_data = super().clean()
        if self.is_valid():
            self._clean_comparison()
        return cleaned_data

    def clean_param_1(self):
        """Validate `param_1` can be found in either the signal `kwargs` or the
        model instance.
        """
        param_1 = self.cleaned_data["param_1"]

        # This isn't the best way to do this. But it's the only way I can think
        # accepting keys in the kwargs.
        # For now we'll accept `created` as this is a common parameter to check
        # on post creation.
        if param_1 == "created":
            return param_1

        valid, _ = get_param_from_obj(param_1, self.instance.signal.model)
        if not valid:
            raise forms.ValidationError(
                f"The model does not have a parameter called {param_1}"
            )
        return param_1

    def _clean_comparison(self):
        """Check that the comparison is valid for the given parameters.
        Depending on what the `comparison` is, it would limit the value for
        `param_1` and `param_2`.

        Note: Due to the order of fields, we need to preprend the underscore
        in the function name and call it manually as `param_2` is cleaned
        after 'comparison'.
        """

        comparison = self.cleaned_data["comparison"]
        param_2 = self.cleaned_data["param_2"]

        if comparison_requires_2_params(comparison) and not param_2:
            raise forms.ValidationError(
                "This comparison requires a second parameter"
            )

        if not comparison_requires_2_params(comparison) and param_2:
            raise forms.ValidationError(
                "This comparison does not require a second parameter"
            )

        return comparison
