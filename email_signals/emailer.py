import typing as _t
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail as _send_mail
from . import utils


def send_mail(
    subject: str,
    recipient_list: _t.Iterable[str],
    plain_message: _t.Optional[str] = None,
    html_message: _t.Optional[str] = None,
    from_email: _t.Optional[str] = None,
    template: _t.Optional[str] = None,
    context: _t.Optional[_t.Dict[str, _t.Any]] = None,
) -> None:
    """A wrapper for Django's `send_email` function. This will handle cases
    where the `from_email` is not defined and where the user wants to use a
    custom template to render their email.

    Args:
        subject: The subject of the email.
        plain_message: The plain text message of the email.
        html_message: The HTML message of the email.
        recipient_list: The list of recipients of the email.
        from_email: The email address of the sender.
        template: The template to use to render the email.
        context: The context to use to render the email.

    Returns:
        None
    """

    try:
        from_email = from_email or settings.EMAIL_SIGNAL_DEFAULT_SENDER
    except AttributeError:
        raise AttributeError(
            "Either `from_email` needs to be set for this model instance. "
            "or `settings.EMAIL_SIGNAL_DEFAULT_SENDER` needs to be set."
        )

    if template:
        html_message = render_to_string(template, context or {})

    _send_mail(
        subject=subject,
        message=utils.add_context_to_string(plain_message, context),
        html_message=utils.add_context_to_string(html_message, context),
        from_email=from_email,
        recipient_list=recipient_list,
    )
