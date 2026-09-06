import unittest
from HHLtools.algorithm import binary_search


class TestAlgorithm(unittest.TestCase):
    def test_binary_search(self):
        lst = [1, 2, 3, 5, 10]
        self.assertEquals(binary_search(lst, 1), 0)
        self.assertEquals(binary_search(lst, 10), 4)
        self.assertEquals(binary_search(lst, 4), -1)
        with self.assertRaises(SystemExit):
            binary_search(1, 10)
