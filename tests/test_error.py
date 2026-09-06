import unittest
from HHLtools.error import raise_error, print_error, UNSET


class TestError(unittest.TestCase):
    def test_raise_error(self):
        with self.assertRaises(SystemExit):
            raise_error(Exception, "")
        print_error(Exception())
        print_error(Exception, "", level=2)
        print_error(Exception, "", level=100)
        print_error(Exception, "")

    def test_unset(self):
        self.assertEquals(str(UNSET), "UNSET")
        self.assertEquals(repr(UNSET), "UNSET")