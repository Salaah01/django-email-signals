from django import forms
from . import models
from .registry import registered_content_types
from .utils import get_param_from_obj
from .constraint_checker import comparision_requires_2_params


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

    def clean_param_2(self):
        """Validate `param_2` can be found in either the signal `kwargs` or the
        model instance.

        If the signal type is `post_save`, `created` is a valid value for
        `param_2`, otherwise, check that the parameter can be found in the
        model instance.
        """
        param_2 = self.cleaned_data['param_2']

        if param_2 == 'created' and self.instance.signal.is_post_save():
            return param_2

        valid, _ = get_param_from_obj(param_2, self.instance)
        if not valid:
            raise forms.ValidationError(
                f"The model does not have a parameter called {param_2}"
            )
        return param_2

    def clean_comparision(self):
        """Validate the comparison is valid for the given parameters.
        Depending on what the `comparision` is, it would limit the value for
        `param_1` and `param_2`.
        """

        comparision = self.cleaned_data['comparision']
        param_1 = self.cleaned_data['param_1']
        param_2 = self.cleaned_data['param_2']

        if comparision_requires_2_params(comparision) and not param_2:
            raise forms.ValidationError(
                "Comparision requires a second parameter"
            )

        if not comparision_requires_2_params(comparision) and param_2:
            raise forms.ValidationError(
                "Comparision does not require a second parameter"
            )

        return comparision
