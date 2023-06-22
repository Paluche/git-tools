"""Module to build logs and formatted output and overlay to print the logs from
the logging built module.
"""

from enum import IntEnum

#
# Global format option
#


# Boolean which make all the color and blinking format from the function below
# enabled or not.
__FORMAT_ENABLED = True

# Boolean which make all the blinking format from the function below enabled or
# not.
__BLINKING_ENABLED = True


#
# String output format utils
#


class Color(IntEnum):
    """The colors you can use in escape sequence formats."""
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7


# pylint: disable-next=invalid-name,too-many-arguments
def get_color_format(reset=True, fg=None, fg_bright=False, bg=None,
                     bg_bright=False, bold=None,  faint=None, italic=None,
                     underline=None):
    """Escape sequence which will make a formatting coloring the text printing
    after it. More information on the different formatting:
        https://en.wikipedia.org/wiki/ANSI_escape_code#Codes

    :param reset: Boolean to indicate to reset all previous format. Defaults to
                  True.
    :param fg: Foreground color. Color of the text printed. If None default
               foreground color from your terminal will be used. Defaults to
                None.
    :param fg_bright: Boolean to indicate to the bright version for the
                      foreground color. Defaults to False.
    :param bg: Background color. If None default background color from your
               terminal will be used. Defaults to None.
    :param bg_bright: Boolean to indicate to the bright version for the
                      background color. Defaults to False.
    :param bold: Boolean to indicate to the enable or disable the bold format
                 on the text. If None the bold format is left untouched. If
                 False it would also disable the faint formatting. Defaults to
                 None.
    :param faint: Boolean to indicate to the enable or disable the faint format
                  on the text. If None faint format is left untouched. If False
                  it would also disable the bold formatting. Defaults to None.
    :param italic: Boolean to indicate to enable or disable the italic format
                   on the text. If None the italic format is left untouched.
                   Defaults to None.
    :param underline: Boolean to indicate to the enable or disable the
                      underline format on the text. If None underline format is
                      left untouched. Defaults to None.

    :return: Escape sequence which will produce the desired format on the text
             which follows it.
    """
    # pylint: disable-next=global-variable-not-assigned
    global __FORMAT_ENABLED

    def _set_color_code(codes, color_base, is_bright, code_modifiers):
        enable, disable = code_modifiers
        if color_base is not None:
            if color_base not in list(Color):
                raise ValueError()

            if is_bright:
                codes.append(enable + color_base)
            else:
                codes.append(disable + color_base)

    codes = []

    if not __FORMAT_ENABLED:
        return ''

    if reset:
        codes.append('0')

    _set_color_code(codes, fg, fg_bright, (90, 30))

    _set_color_code(codes, bg, bg_bright, (100, 40))

    if bold is not None or faint is not None:
        if bold:
            codes.append(1)
        elif faint:
            codes.append(2)
        else:
            codes.append(22)

    if italic is not None:
        if italic:
            codes.append(3)
        else:
            codes.append(23)

    if underline is not None:
        if underline:
            codes.append(4)
        else:
            codes.append(24)

    if codes:
        return '\033[' + ';'.join(f'{code}' for code in codes) + 'm'

    return ''


def get_blink_format(enable):
    """Escape sequence which will make a formatting blink the text printing
    after it. More information on the different formatting:
    https://en.wikipedia.org/wiki/ANSI_escape_code#Codes

    Rendering depends on the terminal used. From some testing on one terminal
    configuration the blinking does not work when background color is set.

    :param enable: Boolean to indicate to the enable or disable the blinking
                   format on the text. If None returns no escape sequence.

    :return: The escape sequence desired.
    """
    # pylint: disable-next=global-variable-not-assigned
    global __FORMAT_ENABLED
    # pylint: disable-next=global-variable-not-assigned
    global __BLINKING_ENABLED

    if enable is None or not __BLINKING_ENABLED or not __FORMAT_ENABLED:
        return ''

    if enable:
        return '\033[5m'

    return '\033[25m'


# pylint: disable-next=invalid-name,too-many-arguments
def get_format(reset=True, fg=None, fg_bright=False, bg=None, bg_bright=False,
               bold=None, faint=None, italic=None, underline=None, blink=None):
    """Escape sequence which will make a formatting. More information on the
    different formatting: https://en.wikipedia.org/wiki/ANSI_escape_code#Codes

    :param reset: Boolean to indicate to reset all previous format. Defaults to
                  True.
    :param fg: Foreground color. Color of the text printed. If None default
               foreground color from your terminal will be used. Defaults to
               None.
    :param fg_bright: Boolean to indicate to the bright version for the
                      foreground color. Defaults to False.
    :param bg: Background color. If None default background color from your
               terminal will be used. Defaults to None.
    :param bg_bright: Boolean to indicate to the bright version for the
                      background color. Defaults to False.
    :param bold: Boolean to indicate to the enable or disable the bold format
                 on the text. If None the bold format is left untouched. If
                 False it would also disable the faint formatting. Defaults to
                 None.
    :param faint: Boolean to indicate to the enable or disable the faint
                  format on the text. If None faint format is left untouched.
                  If False it would also disable the bold formatting. Defaults
                  to None.
    :param italic: Boolean to indicate to enable or disable the italic format
                   on the text. If None the italic format is left untouched.
                   Defaults to None.
    :param underline: Boolean to indicate to the enable or disable the
                      underline format on the text. If None underline format is
                      left untouched. Defaults to None.
    :param blink: Boolean to indicate to the enable or disable the slow blink
                  format on the text. If None blinking format is left
                  untouched. If False it would also disable the fast blink
                  formatting. Defaults to None.

    :return: Escape sequence which will produce the desired format on the text
             which follows it.
    """
    ret = get_color_format(reset=reset, fg=fg, fg_bright=fg_bright,
                           bg=bg, bg_bright=bg_bright, bold=bold,
                           faint=faint, italic=italic, underline=underline)

    ret += get_blink_format(blink)

    return ret


def format_string(*args, **kwargs):
    """Print a message which is formatted with the specified parameters.

    :param *args: Positional arguments to be printed. Like the built-in print()
                  method, each argument is printed separated by a space.
    :param **kwargs: Keyword arguments for the get_format() method.
    """
    if not args:
        return ''

    return (get_format(**kwargs) + ' '.join([str(x) for x in args]) +
            get_format())


def print_format(*args, reset=True, fg=None, fg_bright=None, bg=None,
                 bg_bright=False, bold=None, faint=None, italic=None,
                 underline=None, blink=None, **kwargs):
    """Print a message which is formatted with the specified parameters.

    :param *args: Positional arguments to be printed.
    :param reset: Boolean to indicate to reset all previous format. Defaults to
                  True.
    :param fg_bright: Boolean to indicate to the bright version for the
                      foreground color. Defaults to False.
    :param bg: Background color. If None default background color from your
               terminal will be used. Defaults to None.
    :param bg_bright: Boolean to indicate to the bright version for the
                      background color. Defaults to False.
    :param bold: Boolean to indicate to the enable or disable the bold format
                 on the text. If None the bold format is left untouched. If
                 False it would also disable the faint formatting. Defaults to
                 None.
    :param faint: Boolean to indicate to the enable or disable the faint format
                  on the text. If None faint format is left untouched. If False
                  it would also disable the bold formatting. Defaults to None.
    :param italic: Boolean to indicate to enable or disable the italic format
                   on the text. If None the italic format is left untouched.
                   Defaults to None.
    :param underline: Boolean to indicate to the enable or disable the
                      underline format on the text. If None underline format is
                      left untouched. Defaults to None.
    :param blink: Boolean to indicate to the enable or disable the slow blink
                  format on the text. If None blinking format is left
                  untouched. If False it would also disable the fast blink
                  formatting. Defaults to None.
    :param **kwargs: Additional key-word arguments which will be provided to
                     the builtin method print().
    """
    print(
        format_string(
            *args,
            reset=reset,
            fg=fg,
            fg_bright=fg_bright,
            bg=bg,
            bg_bright=bg_bright,
            bold=bold,
            faint=faint,
            italic=italic,
            underline=underline,
            blink=blink
        ),
        **kwargs
    )
