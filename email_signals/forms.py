from django import forms
from . import models
from .registry import registered_content_types


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
