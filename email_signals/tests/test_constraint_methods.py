from django.test import SimpleTestCase
from .. import constraint_methods


class TestConstraintMethods(SimpleTestCase):
    """Tests the functions in the `constraint_methods` module."""

    def test_exact(self):
        """Tests the `exact` constraint method."""
        self.assertTrue(constraint_methods.exact(1, 1))
        self.assertFalse(constraint_methods.exact(1, 2))

    def test_iexact(self):
        """Tests the `iexact` constraint method."""
        self.assertTrue(constraint_methods.iexact("a", "A"))
        self.assertTrue(constraint_methods.iexact("a", "a"))
        self.assertFalse(constraint_methods.iexact("a", "b"))

    def test_contains(self):
        """Tests the `contains` constraint method."""
        self.assertTrue(constraint_methods.contains("back", "a"))
        self.assertFalse(constraint_methods.contains("a", "b"))

    def test_contains_type_check(self):
        """Tests the `contains` constraint method handles types which are not
        strings.
        """
        self.assertFalse(constraint_methods.contains(1, "a"))
        self.assertFalse(constraint_methods.contains("abc", None))

    def test_icontains(self):
        """Tests the `icontains` constraint method."""
        self.assertTrue(constraint_methods.icontains("BACK", "a"))
        self.assertTrue(constraint_methods.icontains("a", "a"))
        self.assertFalse(constraint_methods.icontains("a", "b"))

    def test_icontains_type_check(self):
        """Tests the `icontains` constraint method handles types which are not
        strings.
        """
        self.assertFalse(constraint_methods.icontains(1, "a"))
        self.assertFalse(constraint_methods.icontains("abc", None))

    def test_gt(self):
        """Tests the `gt` constraint method."""
        self.assertTrue(constraint_methods.gt(2, 1))
        self.assertFalse(constraint_methods.gt(1, 1))
        self.assertFalse(constraint_methods.gt(1, 2))

    def test_gt_type_conversion(self):
        """Tests the `gt` constraint method handles types which are not
        numbers.
        """
        # Should convert to floats and compare successfully.
        self.assertTrue(constraint_methods.gt("1", "0"))
        self.assertFalse(constraint_methods.gt("0", "1"))

        # Should return False if the types cannot be converted.
        self.assertFalse(constraint_methods.gt("a", "b"))

    def test_gte(self):
        """Tests the `gte` constraint method."""
        self.assertTrue(constraint_methods.gte(2, 1))
        self.assertTrue(constraint_methods.gte(1, 1))
        self.assertFalse(constraint_methods.gte(1, 2))

    def test_gte_type_conversion(self):
        """Tests the `gte` constraint method handles types which are not
        numbers.
        """
        # Should convert to floats and compare successfully.
        self.assertTrue(constraint_methods.gte("1", "0"))
        self.assertFalse(constraint_methods.gte("0", "1"))
        self.assertTrue(constraint_methods.gte("1", "1"))

        # Should return False if the types cannot be converted.
        self.assertFalse(constraint_methods.gte("a", "b"))

    def test_lt(self):
        """Tests the `lt` constraint method."""
        self.assertTrue(constraint_methods.lt(1, 2))
        self.assertFalse(constraint_methods.lt(1, 1))
        self.assertFalse(constraint_methods.lt(2, 1))

    def test_lt_type_conversion(self):
        """Tests the `lt` constraint method handles types which are not
        numbers.
        """
        # Should convert to floats and compare successfully.
        self.assertTrue(constraint_methods.lt("0", "1"))
        self.assertFalse(constraint_methods.lt("1", "0"))

        # Should return False if the types cannot be converted.
        self.assertFalse(constraint_methods.lt("a", "b"))

    def test_lte(self):
        """Tests the `lte` constraint method."""
        self.assertTrue(constraint_methods.lte(1, 2))
        self.assertTrue(constraint_methods.lte(1, 1))
        self.assertFalse(constraint_methods.lte(2, 1))

    def test_lte_type_conversion(self):
        """Tests the `lte` constraint method handles types which are not
        numbers.
        """
        # Should convert to floats and compare successfully.
        self.assertTrue(constraint_methods.lte("0", "1"))
        self.assertFalse(constraint_methods.lte("1", "0"))
        self.assertTrue(constraint_methods.lte("1", "1"))

        # Should return False if the types cannot be converted.
        self.assertFalse(constraint_methods.lte("a", "b"))

    def test_startswith(self):
        """Tests the `startswith` constraint method."""
        self.assertTrue(constraint_methods.startswith("abc", "a"))
        self.assertFalse(constraint_methods.startswith("abc", "b"))

    def test_startswith_type_check(self):
        """Tests the `startswith` constraint method handles types which are not
        strings.
        """
        self.assertFalse(constraint_methods.startswith(1, "a"))
        self.assertFalse(constraint_methods.startswith("abc", None))

    def test_istartswith(self):
        """Tests the `istartswith` constraint method."""
        self.assertTrue(constraint_methods.istartswith("ABC", "a"))
        self.assertTrue(constraint_methods.istartswith("abc", "a"))
        self.assertFalse(constraint_methods.istartswith("abc", "b"))

    def test_istartswith_type_check(self):
        """Tests the `istartswith` constraint method handles types which are
        not strings.
        """
        self.assertFalse(constraint_methods.istartswith(1, "a"))
        self.assertFalse(constraint_methods.istartswith("abc", None))

    def test_endswith(self):
        """Tests the `endswith` constraint method."""
        self.assertTrue(constraint_methods.endswith("abc", "c"))
        self.assertFalse(constraint_methods.endswith("abc", "b"))

    def test_endswith_type_check(self):
        """Tests the `endswith` constraint method handles types which are not
        strings.
        """
        self.assertFalse(constraint_methods.endswith(1, "c"))
        self.assertFalse(constraint_methods.endswith("abc", None))

    def test_iendswith(self):
        """Tests the `iendswith` constraint method."""
        self.assertTrue(constraint_methods.iendswith("ABC", "c"))
        self.assertTrue(constraint_methods.iendswith("abc", "c"))
        self.assertFalse(constraint_methods.iendswith("abc", "b"))

    def test_iendswith_type_check(self):
        """Tests the `iendswith` constraint method handles types which are not
        strings.
        """
        self.assertFalse(constraint_methods.iendswith(1, "c"))
        self.assertFalse(constraint_methods.iendswith("abc", None))

    def test_regex(self):
        """Tests the `regex` constraint method."""
        self.assertTrue(constraint_methods.regex("abc", "^a"))
        self.assertFalse(constraint_methods.regex("abc", "^b"))

    def test_iregex(self):
        """Tests the `iregex` constraint method."""
        self.assertTrue(constraint_methods.iregex("Abc1", "^a"))
        self.assertFalse(constraint_methods.iregex("aBc1", "d"))

    def test_isnull(self):
        """Tests the `isnull` constraint method."""
        self.assertTrue(constraint_methods.isnull(None))
        self.assertFalse(constraint_methods.isnull(1))

    def test_isnotnull(self):
        """Tests the `isnotnull` constraint method."""
        self.assertFalse(constraint_methods.isnotnull(None))
        self.assertTrue(constraint_methods.isnotnull(1))

    def test_istrue(self):
        """Tests the `istrue` constraint method."""
        self.assertTrue(constraint_methods.istrue(True))
        self.assertTrue(constraint_methods.istrue("abc"))
        self.assertFalse(constraint_methods.istrue(False))
        self.assertFalse(constraint_methods.istrue(None))
        self.assertFalse(constraint_methods.istrue(""))

    def test_isfalse(self):
        """Tests the `isfalse` constraint method."""
        self.assertTrue(constraint_methods.isfalse(False))
        self.assertTrue(constraint_methods.isfalse(""))
        self.assertFalse(constraint_methods.isfalse(True))
        self.assertFalse(constraint_methods.isfalse("abc"))
        self.assertTrue(constraint_methods.isfalse(None))
