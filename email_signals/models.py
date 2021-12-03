import typing as _t
from django.db import models
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from . registry import add_to_registry


class EmailSignalMixin:
    """A mixin to add a model to the email_signals app."""

    EMAIL_SIGNAL_MODEL = True

    def email_signal_post_init(self) -> None:
        """Add this model to the registry."""
        add_to_registry(self)

    def email_signal_recipients(self, email_opt: int) -> _t.List[str]:
        """Return a list of email addresses to send the signal to."""
        method_name = f'get_email_signal_emails_{email_opt}'
        if not hasattr(self, method_name):
            raise NotImplementedError(
                f'{self.__class__.__name__} has no method {method_name}'
            )
        return getattr(self, method_name)()


class Signal(models.Model):
    """Stores signals to be raised by the email_signals app."""

    class SignalTypeChoices(models.TextChoices):
        """Choices for the type of signal."""
        pre_save = 'pre_save', 'Pre Save'
        post_save = 'post_save', 'Post Save'
        pre_delete = 'pre_delete', 'Pre Delete'
        post_delete = 'post_delete', 'Post Delete'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    plain_text_email = models.TextField(blank=True, null=True)
    html_email = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=255)
    from_email = models.EmailField(
        null=True,
        blank=True,
        help_text='If not set, `settings.EMAIL_SIGNAL_DEFAULT_FROM_EMAIL` \
            with be used.'
    )
    to_emails_opt = models.PositiveIntegerField(
        default=1,
        help_text="The choice of the user to send the email to. For each \
            integer `i`, the method `get_email_signal_emails_<i>` will be \
            called on the model instance. The method should return a list of \
            emails to send to."
    )
    template = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Custom template to use for the email."
    )
    signal_type = models.CharField(
        max_length=20,
        choices=SignalTypeChoices.choices
    )
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'({self.signal_type}): {self.name}'

    def get_signal_type(self):
        """Return the signal type."""
        return getattr(signals, self.signal_type)

    @ classmethod
    def get_signal_type_from_choice(cls, choice: int):
        """Return the signal type from the choice."""
        return getattr(signals, choice)

    @ classmethod
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
            raise ValueError(f'Unknown signal: {signal}')

    @ classmethod
    def get_for_model_and_signal(
        cls,
        instance: 'Signal',
        signal: signals.ModelSignal
    ) -> models.QuerySet['Signal']:
        """Return the signal for the given model and signal type."""
        return cls.objects.filter(
            content_type=ContentType.objects.get_for_model(instance),
            signal_type=cls.get_choice_from_signal(signal),
            active=True,
        )


class SignalConstraint(models.Model):
    """Stores the constraints for a signal."""

    COMPARISION_CHOICES = (
        ('exact', 'Is Equal To'),
        ('iexact', 'Is Equal To (case insensitive)'),
        ('contains', 'Contains'),
        ('icontains', 'Contains (case insensitive)'),
        ('gt', 'Greater Than'),
        ('gte', 'Greater Than or Equal To'),
        ('lt', 'Less Than'),
        ('lte', 'Less Than or Equal To'),
        ('startswith', 'Starts With'),
        ('istartswith', 'Starts With (case insensitive)'),
        ('endswith', 'Ends With'),
        ('iendswith', 'Ends With (case insensitive)'),
        ('regex', 'Matches Regular Expression'),
        ('iregex', 'Matches Regular Expression (case insensitive)'),
        ('isnull', 'Is Null'),
        ('isnotnull', 'Is Not Null'),
        ('istrue', 'Is True'),
        ('isfalse', 'Is False'),
    )

    signal = models.ForeignKey(
        Signal,
        on_delete=models.CASCADE,
        related_name='constraints'
    )
    param_1 = models.CharField(max_length=255)
    comparision = models.CharField(
        max_length=20,
        choices=COMPARISION_CHOICES
    )
    param_2 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.signal.name} - {self.comparision} - {self.param_1}'
