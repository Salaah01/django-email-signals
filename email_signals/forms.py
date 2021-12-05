from django import forms
from . import models
from .registry import registered_content_types
from .utils import get_param_from_obj
from .constraint_checker import comparison_requires_2_params


class SignalAdminForm(forms.ModelForm):

    class Meta:
        model = models.Signal
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Limit the content type choices to the registered content types
        self.fields['content_type'].queryset = registered_content_types()

    def clean_mailing_list(self):
        """The `mailing_list` fill contains a string which corresponds to a
        function that should exist in the model instance. Check that the
        function does exists.
        """
        mailing_list = self.cleaned_data['mailing_list']
        model_class = self.cleaned_data['content_type'].model_class()
        if not hasattr(model_class, mailing_list):
            raise forms.ValidationError(
                f"The model does not have a function called {mailing_list}"
            )
        return mailing_list


class SignalConstraintAdminForm(forms.ModelForm):

    class Meta:
        models = models.SignalConstraint
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if self.is_valid():
            self._clean_comparison()
        return cleaned_data

    def clean_param_1(self):
        """Validate `param_2` can be found in either the signal `kwargs` or the
        model instance.
        """
        param_1 = self.cleaned_data['param_1']

        valid, _ = get_param_from_obj(param_1, self.instance)
        if not valid:
            raise forms.ValidationError(
                f"The model does not have a parameter called {param_1}"
            )
        return param_1

    def _clean_comparison(self):
        """Validate the comparison is valid for the given parameters.
        Depending on what the `comparison` is, it would limit the value for
        `param_1` and `param_2`.

        Note: Due to the order of fields, we need to preprend the underscore
        in the function name and call it manually as `param_2` is cleaned
        after 'comparison'.
        """

        comparison = self.cleaned_data['comparison']
        param_2 = self.cleaned_data['param_2']

        if comparison_requires_2_params(comparison) and not param_2:
            raise forms.ValidationError(
                "This comparison requires a second parameter"
            )

        if not comparison_requires_2_params(comparison) and param_2:
            raise forms.ValidationError(
                "This comparison does not require a second parameter"
            )

        return comparison