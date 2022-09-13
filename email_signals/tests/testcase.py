import typing as _t
from pathlib import Path
from django.test import TestCase
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from ..models import Signal
from ..registry import add_to_registry
from ..signals import setup as signals_setup


def setup_settings():
    """Helper function to parts of the settings that are used in the tests."""
    settings.TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [Path(__file__).resolve().parent.parent.parent],
        }
    ]


class EmailSignalTestCase(TestCase):
    """Wrapper for the Django testcase. Will handle the test models setup
    and teardown.
    """

    @classmethod
    def setUpClass(cls):
        from . import models

        models.TestCustomerModel.create_table()
        models.TestCustomerOrderModel.create_table()
        models.TestM2MModel.create_table()
        models.TestOne2OneModel.create_table()

        cls.Customer = models.TestCustomerModel
        cls.CustomerOrder = models.TestCustomerOrderModel
        cls.M2MModel = models.TestM2MModel
        cls.One2OneModel = models.TestOne2OneModel

        setup_settings()
        super().setUpClass()

    def setUp(self):
        self.customer_rec = self.Customer.create_record()
        self.customer_order_rec = self.CustomerOrder.create_record(
            self.customer_rec
        )

    @classmethod
    def tearDownClass(cls):
        cls.CustomerOrder.drop_table()
        cls.M2MModel.drop_table()
        cls.One2OneModel.drop_table()
        cls.Customer.drop_table()
        super().tearDownClass()

    def tearDown(self):
        self.CustomerOrder.objects.all().delete()
        self.M2MModel.objects.all().delete()
        self.One2OneModel.objects.all().delete()
        self.Customer.objects.all().delete()
        super().tearDown()

    def setup_signals(self):
        """Adds the test models to the signal registry and enables to signals
        to be raised.
        """
        add_to_registry(self.Customer)
        add_to_registry(self.CustomerOrder)
        signals_setup()

    @staticmethod
    def create_signal(
        model_instance: models.Model,
        signal_type: Signal.SignalTypeChoices = Signal.SignalTypeChoices.pre_save,  # noqa E501
        name: str = "Test Signal",
        content_type: _t.Optional[ContentType] = None,
        from_email: str = "test@email.com",
        subject: str = "Test Subject",
        template: _t.Optional[str] = None,
        mailing_list: str = "my_mailing_list",
    ) -> Signal:
        """Create a signal record for a model instance and signal type.

        Args:
            model_instance (models.Model): The model instance to create a
                signal for.
            signal_type (Signal.SignalTypeChoices): The signal type to create
                for the model instance.
            name (str, optional): The name of the signal. Defaults to
                'Test Signal'.
            content_type (ContentType, optional): The content type of the
                model instance. Defaults to the content type of the instance
                provided.
            from_email (str, optional): The from email address to use for
                the signal. Defaults to 'test@email.com'.
            subject (str, optional): The subject of the signal. Defaults to
                'Test Subject'.
            template (str, optional): The template to use for the signal.
        """
        rec = Signal.objects.create(
            name=name,
            content_type=content_type
            or ContentType.objects.get_for_model(model_instance),
            signal_type=signal_type,
            from_email=from_email,
            subject=subject,
            template=template,
            mailing_list=mailing_list,
        )
        rec.save()
        return rec
