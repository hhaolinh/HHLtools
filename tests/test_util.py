import unittest
from HHLtools.utils import *


class TestUtil(unittest.TestCase):
    def test_get_type_name(self):
        self.assertEquals(get_type_name(1), "int")

    def test_get_type_name_from_annotation(self):
        self.assertEquals(get_type_name_from_annotation(Any), "Any")

    def test_check_type_from_annotation(self):
        self.assertTrue(check_type_from_annotation(Any, 1))
        self.assertTrue(check_type_from_annotation(str, UNSET))
        self.assertTrue(check_type_from_annotation(str, "1"))
        with self.assertRaises(NotImplementedError):
            check_type_from_annotation(list[int], [1, 2, 3])
