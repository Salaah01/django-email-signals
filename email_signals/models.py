import typing as _t
from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField


class EmailSignalMixin:
    """A mixin to add a model to the email_signals app."""

    EMAIL_SIGNAL_MODEL = True

    def email_signal_recipients(self, method_name: str) -> _t.List[str]:
        """Return a list of email addresses to send the signal to.

        Args:
            method_name: The name of the method which when called will return
                a mailing list.

        Returns:
            A list of email addresses to send emails to.

        """
        emails = None
        if hasattr(self, method_name):
            emails = getattr(self, method_name)()
        elif "@" in method_name:
            emails = method_name.split(",")
            emails = [email.strip() for email in emails if email]
        if emails is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} has no method {method_name} or "
                f"{method_name} is not a list of emails"
            )
        return emails


class Signal(models.Model):
    """Stores signals to be raised by the email_signals app."""

    class SignalTypeChoices(models.TextChoices):
        """Choices for the type of signal."""

        pre_save = "pre_save", "Pre Save"
        post_save = "post_save", "Post Save"
        pre_delete = "pre_delete", "Pre Delete"
        post_delete = "post_delete", "Post Delete"

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Model",
    )
    plain_message = models.TextField(
        blank=True,
        null=True,
        verbose_name="Plain text content",
    )
    html_message = RichTextField(
        blank=True,
        null=True,
        verbose_name="HTML content",
    )
    subject = models.CharField(max_length=255)
    from_email = models.EmailField(
        null=True,
        blank=True,
        help_text="If not set, `settings.EMAIL_SIGNAL_DEFAULT_SENDER` "
        "with be used.",
    )
    mailing_list = models.TextField(
        help_text="The mailing list to send the signal to. Either enter a "
        "comma separated list of emails or the app will search for a function "
        "with the same name in the model instance.",
    )
    template = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Custom template to use for the email. (Paths relative to \
            `settings.TEMPLATES[i]['DIRS']`)",
    )
    signal_type = models.CharField(
        max_length=20,
        choices=SignalTypeChoices.choices,
    )
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"({self.signal_type}): {self.name}"

    def get_signal_type(self) -> signals.ModelSignal:
        """Return the signal type."""
        return getattr(signals, self.signal_type)

    @classmethod
    def get_choice_from_signal(cls, signal: signals.ModelSignal) -> str:
        """Return the signal type from the signal."""
        if signal == signals.pre_save:
            return cls.SignalTypeChoices.pre_save
        elif signal == signals.post_save:
            return cls.SignalTypeChoices.post_save
        elif signal == signals.pre_delete:
            return cls.SignalTypeChoices.pre_delete
        elif signal == signals.post_delete:
            return cls.SignalTypeChoices.post_delete
        else:
            raise ValueError(f"Unknown signal: {signal}")

    @classmethod
    def get_for_model_and_signal(
        cls, instance: "Signal", signal: signals.ModelSignal
    ) -> models.QuerySet["Signal"]:
        """Return the signal for the given model and signal type."""
        return cls.objects.filter(
            content_type=ContentType.objects.get_for_model(instance),
            signal_type=cls.get_choice_from_signal(signal),
            active=True,
        )

    @property
    def constraints_count(self) -> int:
        """Return the number of constraints."""
        return self.constraints.count()

    @property
    def model(self) -> models.base.ModelBase:
        """Return the model of the signal."""
        return self.content_type.model_class()

    def is_pre_save(self) -> bool:
        """Return `True` if the signal is a pre save signal."""
        return self.signal_type == self.SignalTypeChoices.pre_save

    def is_post_save(self) -> bool:
        """Return `True` if the signal is a post save signal."""
        return self.signal_type == self.SignalTypeChoices.post_save

    def is_pre_delete(self) -> bool:
        """Return `True` if the signal is a pre delete signal."""
        return self.signal_type == self.SignalTypeChoices.pre_delete

    def is_post_delete(self) -> bool:
        """Return `True` if the signal is a post delete signal."""
        return self.signal_type == self.SignalTypeChoices.post_delete


class SignalConstraint(models.Model):
    """Stores the constraints for a signal."""

    COMPARISON_CHOICES = (
        ("exact", "Is Equal To"),
        ("iexact", "Is Equal To (case insensitive)"),
        ("contains", "Contains"),
        ("icontains", "Contains (case insensitive)"),
        ("gt", "Greater Than"),
        ("gte", "Greater Than or Equal To"),
        ("lt", "Less Than"),
        ("lte", "Less Than or Equal To"),
        ("startswith", "Starts With"),
        ("istartswith", "Starts With (case insensitive)"),
        ("endswith", "Ends With"),
        ("iendswith", "Ends With (case insensitive)"),
        ("regex", "Matches Regular Expression"),
        ("iregex", "Matches Regular Expression (case insensitive)"),
        ("isnull", "Is Null"),
        ("isnotnull", "Is Not Null"),
        ("istrue", "Is True"),
        ("isfalse", "Is False"),
    )

    signal = models.ForeignKey(
        Signal, on_delete=models.CASCADE, related_name="constraints"
    )
    param_1 = models.CharField(
        max_length=255,
        verbose_name="Parameter 1",
        help_text='Will be searched in the instance and signal kwargs recursively. Use "." to show a layer in each attribute.',  # noqa E501
    )
    comparison = models.CharField(max_length=20, choices=COMPARISON_CHOICES)
    param_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Parameter 2",
        help_text='Will be searched in the instance and signal kwargs recursively. Use "." to show a layer in each attribute. Also supports primitive values.',  # noqa E501
    )

    def __str__(self) -> str:
        return f"{self.signal.name} - {self.comparison} - {self.param_1}"
