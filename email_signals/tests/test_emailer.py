from django.test import SimpleTestCase
from django.core import mail
from .testcase import setup_settings
from .. import emailer


class TestSendMail(SimpleTestCase):
    """Unittests for the `send_mail` function in the `emailer` module."""

    def test_send_mail_no_template(self):
        """Tests that the function is able to send an email without a
        template."""
        emailer.send_mail(
            subject="Test Subject",
            plain_message="Test Message",
            html_message="<p>Test Message</p>",
            recipient_list=["test@test.com"],
            from_email="test@test.com",
        )
        self.assertEqual(len(mail.outbox), 1)

    def test_send_mail_with_template(self):
        """Tests that the function is able to send an email with a template."""

        setup_settings()

        emailer.send_mail(
            subject="Test Subject",
            plain_message="Test Message",
            html_message="<p>Test Message</p>",
            recipient_list=["test@test.com"],
            from_email="test@test.com",
            template="email_signals/tests/test_emailer.html",
        )
        self.assertEqual(len(mail.outbox), 1)
