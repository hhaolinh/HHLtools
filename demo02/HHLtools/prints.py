from HHLtools.Herror import *


class FontStyle:
    DEFAULT = 0
    BOLD = 1
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7


class FontColor:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37


class BackgroundColor:
    DEFAULT = 0
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47


def prints(content, fontStyle=None, fontColor=None, backgroundColor=None):
    codes = []
    if fontStyle is not None and fontStyle != 0:
        codes.append(str(fontStyle))
    if fontColor is not None:
        codes.append(str(fontColor))
    if backgroundColor is not None:
        codes.append(str(backgroundColor))
    print(f"\033[{';'.join(codes)}m{content}\033[0m")