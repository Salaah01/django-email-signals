from types import SimpleNamespace
from django.test import SimpleTestCase
from .. import utils
from .testcase import EmailSignalTestCase


class TestConvertToPrimitive(SimpleTestCase):
    """Unittests for the `convert_to_primitive` utility function."""

    def test_convert_to_true(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is 'true'
        """
        self.assertEqual(utils.convert_to_primitive("true"), True)
        self.assertEqual(utils.convert_to_primitive("tRuE"), True)

    def test_convert_to_false(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is 'false'
        """
        self.assertEqual(utils.convert_to_primitive("false"), False)
        self.assertEqual(utils.convert_to_primitive("fAlSe"), False)

    def test_convert_to_none(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is 'none'
        """
        self.assertEqual(utils.convert_to_primitive("none"), None)
        self.assertEqual(utils.convert_to_primitive("nOnE"), None)
        self.assertEqual(utils.convert_to_primitive("null"), None)
        self.assertEqual(utils.convert_to_primitive("nuLL"), None)

    def test_convert_to_float(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is a float
        """
        self.assertEqual(utils.convert_to_primitive("1.0"), 1.0)
        self.assertEqual(utils.convert_to_primitive("1.1"), 1.1)

    def test_convert_to_bad_float(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is not a flat but has a '.' in it. It should return the value back as
        a string.
        """
        self.assertEqual(utils.convert_to_primitive("1.1.1"), "1.1.1")

    def test_convert_to_int(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is an int
        """
        self.assertEqual(utils.convert_to_primitive("1"), 1)
        self.assertEqual(utils.convert_to_primitive("2"), 2)

    def test_failed_convert_to_primitive(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is not a valid value.
        """
        self.assertEqual(utils.convert_to_primitive("a"), "a")


class TestGetParamFromObj(EmailSignalTestCase):
    """Unittests for the `get_param_from_obj` utility function."""

    def test_dict(self):
        """Test the function returns the current value from a `dict`."""
        self.assertEqual(utils.get_param_from_obj("a", {"a": 1}), (True, 1))

    def test_multi_layered_dict(self):
        """Test the function returns the current value from a `dict`."""
        self.assertEqual(
            utils.get_param_from_obj("a.b.c", {"a": {"b": {"c": 1}}}),
            (True, 1),
        )

    def test_iterable(self):
        """Test the function returns the current value from a iterable."""
        self.assertEqual(utils.get_param_from_obj("0", [1, 2]), (True, 1))
        self.assertEqual(utils.get_param_from_obj("0", (1, 2)), (True, 1))

    def test_multi_layered_iterable(self):
        """Test the function returns the current value from a iterable."""
        self.assertEqual(
            utils.get_param_from_obj("0.1", [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
            (True, 2),
        )
        self.assertEqual(
            utils.get_param_from_obj("0.1", ((1, 2, 3), (4, 5, 6), (7, 8, 9))),
            (True, 2),
        )

    def test_simplenamespace(self):
        """Test the function returns the current value from a `SimpleNamespace`
        object.
        """
        self.assertEqual(
            utils.get_param_from_obj("a", SimpleNamespace(a=1)),
            (True, 1),
        )

    def test_model_instance(self):
        """Test that the function is able to travel into a model instance."""

        self.Customer.objects.create(name="Util Test Customer").save()

        self.assertEqual(
            utils.get_param_from_obj(
                "0.name",
                self.Customer.objects.filter(name="Util Test Customer"),
            ),
            (True, "Util Test Customer"),
        )


class TestGetModelAttrNames(EmailSignalTestCase):
    """Unittests for the `get_model_attr_names` utility function."""

    def test_get_model_attr_names_customer(self):
        """Test the `get_model_attr_names` function contains the correct
        attributes when provided the customer model."""
        model_attr_names = utils.get_model_attr_names(self.Customer)

        for field in ("id", "name", "email"):
            self.assertIn(field, model_attr_names)

    def test_get_model_attr_names_customer_order(self):
        """Test the `get_model_attr_names` function contains the correct
        attributes when provided the customer order model."""

        model_attr_names = utils.get_model_attr_names(self.CustomerOrder)

        for field in ("customer", "order_number"):
            self.assertIn(field, model_attr_names)

        for field in ("name", "email"):
            self.assertIn(field, model_attr_names["customer"])

    def test_get_model_attrs_m2m_model(self):
        """Test the `get_model_attr_names` function contains the correct
        attributes when provided the test M2M model."""

        model_attr_names = utils.get_model_attr_names(self.M2MModel)

        for field in ("id", "customers", "fav_colour"):
            self.assertIn(field, model_attr_names)

    def test_get_model_attrs_one2one_model(self):
        """Test the `get_model_attr_names` function contains the correct
        attributes when provided the test one2one model."""

        model_attr_names = utils.get_model_attr_names(self.One2OneModel)

        for field in ("id", "customer", "age"):
            self.assertIn(field, model_attr_names)

        for field in ("id", "name", "email"):
            self.assertIn(field, model_attr_names["customer"])


class TestAddContextToString(EmailSignalTestCase):
    """Unittests for the `add_context_to_string` utility function."""

    def test_with_nested_dict(self):
        """Test the `add_context_to_string` function works with a nested
        dict.
        """
        self.assertEqual(
            utils.add_context_to_string("test {{ a.a }}", {"a": {"a": 1}}),
            "test 1",
        )

    def test_with_nested_list(self):
        """Test the `add_context_to_string` function works with a list."""
        self.assertEqual(
            utils.add_context_to_string("test {{ a.1 }}", {"a": [1, 2, 3]}),
            "test 2",
        )

    def test_with_model(self):
        """Test the `add_context_to_string` function works with a model."""

        self.assertEqual(
            utils.add_context_to_string(
                "test {{ order.customer.name }}",
                {
                    "order": self.customer_order_rec,
                },
            ),
            f"test {self.customer_rec.name}",
        )

    def test_with_missing_context(self):
        """Test that the `add_context_to_string` function replaces missing
        context with an empty string.
        """
        self.assertEqual(
            utils.add_context_to_string("test {{ a.a }}", {}),
            "test ",
        )
