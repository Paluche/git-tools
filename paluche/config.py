"""Utils regarding the loading and parsing of the git_tools_rc file.
Configuring the scripts.
"""

import os
from configparser import ConfigParser, Error
from paluche.logging import Color

DEFAULT_RC = {
    'git-branch-status': {
        'branch_owner': '',
        'my-branches-color': Color.BLUE,
        'default-branch-color': Color.YELLOW,
        'branches-color': Color.MAGENTA,
        'corner-high-left': '┌',
        'corner-high-right': '┐',
        'corner-low-left': '└',
        'corner-low-right': '┘',
        'cross-high': '┬',
        'cross-middle': '┼',
        'cross-low': '┴',
        'cross-left': '├',
        'cross-right': '┤',
        'line-horizontal': '─',
        'line-vertical': '│',
        'cursor': '*',
        'rebased': '',
        'not-rebased': '',
        'ahead': 'ahead',
        'behind': 'behind',
        'up-to-date': 'up-to-date',
    },
}


def _has_git_tools_rc(*args, dot_file=False):
    if not all(args):
        # One of the argument is None, the path will be invalid.
        return None

    name = ('.' if dot_file else '') + 'git_tools_rc'
    path = os.path.join(*args, name)

    if os.path.isfile(path):
        return path

    return None


def _find_git_tools_rc():
    home = os.environ.get('HOME', os.path.expanduser('~'))

    search_paths = {
        ((os.environ.get('XDG_CONFIG_HOME'), ), False),
        ((home, '.config'), False),
        ((home, ), True),
        (('/etc', 'git-tools-rc'), False),
    }

    for search_path, dot_file in search_paths:
        if path := _has_git_tools_rc(*search_path, dot_file=dot_file):
            return path

    return None


def load_git_tools_rc():
    """Search and load for the git_tools_rc files in the following locations:
    - ${XDG_CONFIG_HOME}/git_tools_rc
    - ${HOME}/.config/git_tools_rc
    - ${HOME}/.git_tools_rc
    - /etc/git-tools-rc
    """
    path = _find_git_tools_rc()
    ret = DEFAULT_RC.copy()

    if not path:
        return ret

    try:
        config_parser = ConfigParser()

        with open(path, mode='r', encoding='utf-8') as rc_file:
            config_parser.read_file(rc_file)
    except Error:
        return ret

    for section_key, section in config_parser.items():
        if section_key == 'DEFAULT':
            continue

        if section_key not in DEFAULT_RC:
            raise ValueError(
                f'Unexpected section {section_key} in git_tools_rc'
            )

        allowed_keys = list(DEFAULT_RC[section_key])

        for key, value in section.items():
            if key not in allowed_keys:
                raise ValueError(
                    f'Unexpected key "{key}" in section "{section_key}" '
                    f'{path}'
                )

            if 'color' in key:
                # The setting is referring to a color so must be a valid
                # Color attribute.
                if not hasattr(Color, value):
                    raise ValueError(
                        f'Invalid color settings {value}'
                    )

                value = getattr(Color, value)

            ret[section_key][key] = value

    return ret
