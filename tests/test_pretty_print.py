import unittest
from HHLtools.prettyprint import *


class TestPrettyPrint(unittest.TestCase):
    def test_prints(self):
        self.assertIsNone(prints("123", backgroundColor=BackgroundColor.GREEN, fontColor=FontColor.BLUE, fontStyle=FontStyle.BLINK))
