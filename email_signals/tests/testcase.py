from django.test import TestCase
from django.db import models, connection
from django.contrib.contenttypes.models import ContentType
from ..models import Signal


class EmailSignalTestCase(TestCase):
    """Wrapper for the Django testcase. Will handle the test models setup
    and teardown.
    """

    @classmethod
    def setUpClass(cls):
        from .models import TestCustomerModel, TestCustomerOrderModel

        TestCustomerModel.create_table()
        TestCustomerOrderModel.create_table()
        cls.Customer = TestCustomerModel
        cls.CustomerOrder = TestCustomerOrderModel
        super().setUpClass()

    def setUp(self):
        self.customer_rec = self.Customer.create_record()
        self.customer_order_rec = self.CustomerOrder.create_record(
            self.customer_rec
        )

    @classmethod
    def tearDownClass(cls):
        cls.CustomerOrder.drop_table()
        cls.Customer.drop_table()
        super().tearDownClass()

    def tearDown(self):
        self.CustomerOrder.objects.all().delete()
        self.Customer.objects.all().delete()
        super().tearDown()

    @staticmethod
    def create_signal(
        model_instance: models.Model,
        signal_type: Signal.SignalTypeChoices = Signal.SignalTypeChoices.pre_save,
    ) -> Signal:
        """Create a signal record for a model instance and signal type.

        Args:
            model_instance (models.Model): The model instance to create a
                signal for.
            signal_type (Signal.SignalTypeChoices): The signal type to create
                for the model instance.
        """
        rec = Signal.objects.create(
            name='Test Signal',
            content_type=ContentType.objects.get_for_model(model_instance),
            signal_type=signal_type,
            from_email='test@email.com',
            subject='Test Subject',
        )
        rec.save()
        return rec
