import typing as _t
from django.contrib.contenttypes.models import ContentType
from .testcase import EmailSignalTestCase
from ..forms import SignalAdminForm
from ..registry import add_to_registry


class TestSignalAdminForm(EmailSignalTestCase):
    """Unitests for the `SignalAdminForm` class."""

    @classmethod
    def setUpClass(cls):
        """Creates a table for the model."""
        super().setUpClass()
        add_to_registry(cls.Customer)

    def sample_form(
        self, override_form_data: _t.Optional[dict] = None
    ) -> SignalAdminForm:
        form_data = {
            "name": "Test Signal",
            "description": "Test description",
            "content_type": ContentType.objects.get_for_model(
                self.customer_rec
            ).pk,
            "plain_message": "Test plain message",
            "html_message": "Test html message",
            "subject": "Test subject",
            "from_email": "test@email.com",
            "mailing_list": "my_mailing_list",
            "template": None,
            "signal_type": "pre_save",
        }
        form_data.update(override_form_data or {})
        form = SignalAdminForm(data=form_data)
        form.is_valid()
        return form

    def test_valid_form(self):
        """Basic test to check that a valid form is accepted."""
        form = self.sample_form()
        self.assertTrue(form.is_valid(), form.data)

    def test_invalid_mailing_list(self):
        """Test form where an invalid `mailing_list` is provided."""
        form = self.sample_form({"mailing_list": "invalid"})
        self.assertFalse(form.is_valid())

    def test_email_mailing_list(self):
        """Test form where an email list `mailing_list` is provided."""
        form = self.sample_form(
            {"mailing_list": "test@email.com,test1@email.com"}
        )
        self.assertTrue(form.is_valid())

    def test_invalid_template(self):
        """Test form where an invalid `template` is provided."""
        form = self.sample_form({"template": "invalid"})
        self.assertFalse(form.is_valid())

    def test_valid_template(self):
        """Test form where a valid `template` is provided."""
        form = self.sample_form(
            {"template": "email_signals/tests/test_emailer.html"}
        )
        self.assertTrue(form.is_valid(), form.data)
