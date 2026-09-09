"""Terminal formatting and tree-display constants."""


class FontStyle:
    """ANSI Select Graphic Rendition codes for font styles."""

    DEFAULT = 0
    BOLD = 1
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7


class FontColor:
    """ANSI foreground-color codes."""

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    WHITE = 37


class BackgroundColor:
    """ANSI background-color codes."""

    DEFAULT = 0
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    WHITE = 47


class TreeConnectors:
    """Unicode connectors used to render tree-shaped output."""

    LONG = "├── "
    SHORT = "└── "
    STRAIGHT = "│   "
    CONTINUATION = "    "
    RECURSION = "↻ "


def prints(content, *args, fontStyle=None, fontColor=None, backgroundColor=None, **kwargs):
    """Print content with optional ANSI terminal formatting.

    Positional and keyword arguments not used for styling are forwarded to
    :func:`print`.

    :param content: Value to print.
    :param args: Additional positional arguments forwarded to :func:`print`.
    :param fontStyle: ANSI font-style code, such as :attr:`FontStyle.BOLD`.
    :param fontColor: ANSI foreground-color code, such as
        :attr:`FontColor.RED`.
    :param backgroundColor: ANSI background-color code, such as
        :attr:`BackgroundColor.BLUE`.
    :param kwargs: Additional keyword arguments forwarded to :func:`print`.
    """
    codes = []
    if fontStyle is not None and fontStyle != 0:
        codes.append(str(fontStyle))
    if fontColor is not None:
        codes.append(str(fontColor))
    if backgroundColor is not None:
        codes.append(str(backgroundColor))
    print(f"\033[{';'.join(codes)}m{content}\033[0m", *args, **kwargs)
