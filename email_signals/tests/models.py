import typing as _t
import random
import string
from django.db import connection, models
from django.contrib.contenttypes.models import ContentType
from ..models import EmailSignalMixin


def generate_random_string() -> str:
    """Generates a random string."""
    return "".join(
        random.choice(string.ascii_letters)
        for _ in range(random.randint(3, 10))
    )


def generate_random_email() -> str:
    """Generates a random email."""
    return f"{generate_random_string()}@{generate_random_string()}.com"


class TestCustomerModel(models.Model, EmailSignalMixin):
    """A model used to testing purposes. It will imitate a customer model."""

    name = models.CharField(max_length=200, default=generate_random_string)
    email = models.CharField(max_length=200, default=generate_random_email)

    def my_mailing_list(self) -> _t.List[str]:
        return [self.email]

    @classmethod
    def create_table(cls) -> None:
        """Creates the table in the database."""
        if cls._meta.db_table not in connection.introspection.table_names():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls)
            ContentType.objects.get_or_create(
                app_label="email_signals",
                model="testcustomermodel",
            )

    @classmethod
    def drop_table(cls) -> None:
        """Drops the table from the database."""
        if cls._meta.db_table in connection.introspection.table_names():
            with connection.cursor() as cursor:
                cursor.execute(
                    "DROP TABLE IF EXISTS {};".format(cls._meta.db_table)
                )
            ContentType.objects.filter(
                app_label="email_signals",
                model="testcustomermodel",
            ).delete()

    @classmethod
    def create_record(cls) -> "TestCustomerModel":
        """Creates a record in the database."""
        rec = cls.objects.create()
        rec.save()
        return rec


class TestCustomerOrderModel(models.Model, EmailSignalMixin):
    """A model used to testing purposes. It will imitate a customer order
    model.
    """

    customer = models.ForeignKey(TestCustomerModel, on_delete=models.CASCADE)
    order_number = models.CharField(
        max_length=100, default=generate_random_string, null=True, blank=True
    )

    def my_mailing_list(self) -> _t.List[str]:
        return [self.customer.email]

    @classmethod
    def create_table(cls) -> None:
        """Creates the table in the database."""
        if cls._meta.db_table not in connection.introspection.table_names():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls)
            ContentType.objects.get_or_create(
                app_label="email_signals",
                model="testcustomerordermodel",
            )

    @classmethod
    def drop_table(cls) -> None:
        """Drops the table from the database."""
        if cls._meta.db_table in connection.introspection.table_names():
            with connection.cursor() as cursor:
                cursor.execute(
                    "DROP TABLE IF EXISTS {};".format(cls._meta.db_table)
                )
            ContentType.objects.filter(
                app_label="email_signals",
                model="testcustomerordermodel",
            ).delete()

    @classmethod
    def create_record(
        cls, customer: TestCustomerModel
    ) -> "TestCustomerOrderModel":
        """Creates a record in the database."""
        rec = cls.objects.create(customer=customer)
        rec.save()
        return rec


class TestM2MModel(models.Model, EmailSignalMixin):
    """A model used to testing purposes. It will imitate a m2m model."""

    customers = models.ManyToManyField(
        TestCustomerModel, related_name="fav_colors"
    )
    fav_colour = models.CharField(
        max_length=50, default=generate_random_string
    )

    @classmethod
    def create_table(cls) -> None:
        """Creates the table in the database."""
        if cls._meta.db_table not in connection.introspection.table_names():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls)
            ContentType.objects.get_or_create(
                app_label="email_signals",
                model="testM2MModel",
            )

    @classmethod
    def drop_table(cls) -> None:
        """Drops the table from the database."""
        if cls._meta.db_table in connection.introspection.table_names():
            with connection.cursor() as cursor:
                cursor.execute(
                    "DROP TABLE IF EXISTS {};".format(cls._meta.db_table)
                )
            ContentType.objects.filter(
                app_label="email_signals",
                model="testM2MModel",
            ).delete()

    @classmethod
    def create_record(cls, customer: TestCustomerModel) -> "TestM2MModel":
        """Creates a record in the database."""
        rec = cls.objects.create(customer=customer)
        rec.save()
        return rec


class TestOne2OneModel(models.Model, EmailSignalMixin):
    """A model used to testing purposes. It will imitate a one-to-one
    relation.
    """

    customer = models.OneToOneField(
        TestCustomerModel, on_delete=models.CASCADE
    )
    age = models.IntegerField(default=10)

    @classmethod
    def create_table(cls) -> None:
        """Creates the table in the database."""
        if cls._meta.db_table not in connection.introspection.table_names():
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls)
            ContentType.objects.get_or_create(
                app_label="email_signals",
                model="testone2onemodel",
            )

    @classmethod
    def drop_table(cls) -> None:
        """Drops the table from the database."""
        if cls._meta.db_table in connection.introspection.table_names():
            with connection.cursor() as cursor:
                cursor.execute(
                    "DROP TABLE IF EXISTS {};".format(cls._meta.db_table)
                )
            ContentType.objects.filter(
                app_label="email_signals",
                model="testone2onemodel",
            ).delete()

    @classmethod
    def create_record(cls, customer: TestCustomerModel) -> "TestOne2OneModel":
        """Creates a record in the database."""
        rec = cls.objects.create(customer=customer)
        rec.save()
        return rec
