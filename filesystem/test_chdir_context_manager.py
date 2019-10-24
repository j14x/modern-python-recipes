"""
Tests for 'chdir_context_manager'
"""


from pathlib import Path

from fsforge import create_fs

from chdir_context_manager import ChangeDir


FORGED_HOME = {
    'a_user': {
        '.bashrc': None,
        'cv.tex': None,
        'doc.txt': None,
        'code': {
            'program1.py': None,
            'program2.c': None,
        }
    }
}


def test_context_manager(fs):
    create_fs(fs, FORGED_HOME, 'home/')

    source = Path('/home')
    destination = source / 'a_user/code/'
    code = FORGED_HOME['a_user']['code']
    forged_entries = [entry for entry in code.keys()]

    with ChangeDir(destination, source) as cwd:
        entries = [entry.name for entry in cwd]

        assert cwd.destination() == destination
        assert cwd.source() == source
        assert Path.cwd() == destination
        assert entries == forged_entries
    assert Path.cwd() == source
