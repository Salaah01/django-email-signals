from types import SimpleNamespace
from django.test import SimpleTestCase
from .testcase import EmailSignalTestCase
from .. import utils
from ..models import SignalConstraint


class TestConvertToPrimitive(SimpleTestCase):
    """Unittests for the `convert_to_primitive` utility function."""

    def test_convert_to_true(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is 'true'
        """
        self.assertEqual(utils.convert_to_primitive('true'), True)
        self.assertEqual(utils.convert_to_primitive('tRuE'), True)

    def test_convert_to_false(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is 'false'
        """
        self.assertEqual(utils.convert_to_primitive('false'), False)
        self.assertEqual(utils.convert_to_primitive('fAlSe'), False)

    def test_convert_to_none(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is 'none'
        """
        self.assertEqual(utils.convert_to_primitive('none'), None)
        self.assertEqual(utils.convert_to_primitive('nOnE'), None)
        self.assertEqual(utils.convert_to_primitive('null'), None)
        self.assertEqual(utils.convert_to_primitive('nuLL'), None)

    def test_convert_to_float(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is a float
        """
        self.assertEqual(utils.convert_to_primitive('1.0'), 1.0)
        self.assertEqual(utils.convert_to_primitive('1.1'), 1.1)

    def test_convert_to_bad_float(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is not a flat but has a '.' in it. It should return the value back as
        a string.
        """
        self.assertEqual(utils.convert_to_primitive('1.1.1'), '1.1.1')

    def test_convert_to_int(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is an int
        """
        self.assertEqual(utils.convert_to_primitive('1'), 1)
        self.assertEqual(utils.convert_to_primitive('2'), 2)

    def test_failed_convert_to_primitive(self):
        """Test the `convert_to_primitive` method where the paramater provided
        is not a valid value.
        """
        self.assertEqual(utils.convert_to_primitive('a'), 'a')


class TestGetParamFromObj(EmailSignalTestCase):
    """Unittests for the `get_param_from_obj` utility function."""

    def test_dict(self):
        """Test the function returns the current value from a `dict`."""
        self.assertEqual(utils.get_param_from_obj('a', {'a': 1}), (True, 1))

    def test_multi_layered_dict(self):
        """Test the function returns the current value from a `dict`."""
        self.assertEqual(
            utils.get_param_from_obj('a.b.c', {'a': {'b': {'c': 1}}}),
            (True, 1),
        )

    def test_iterable(self):
        """Test the function returns the current value from a iterable."""
        self.assertEqual(utils.get_param_from_obj('0', [1, 2]), (True, 1))
        self.assertEqual(utils.get_param_from_obj('0', (1, 2)), (True, 1))

    def test_multi_layered_iterable(self):
        """Test the function returns the current value from a iterable."""
        self.assertEqual(
            utils.get_param_from_obj(
                '0.1',
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            ),
            (True, 2),
        )
        self.assertEqual(
            utils.get_param_from_obj(
                '0.1',
                ((1, 2, 3), (4, 5, 6), (7, 8, 9))
            ),
            (True, 2),
        )

    def test_simplenamespace(self):
        """Test the function returns the current value from a `SimpleNamespace`
        object.
        """
        self.assertEqual(
            utils.get_param_from_obj('a', SimpleNamespace(a=1)),
            (True, 1),
        )

    def test_model_instance(self):
        """Test that the function is able to travel into a model instance."""

        self.Customer.objects.create(name='Util Test Customer').save()

        self.assertEqual(
            utils.get_param_from_obj(
                '0.name',
                self.Customer.objects.filter(name='Util Test Customer')
            ),
            (True, 'Util Test Customer'),
        )
