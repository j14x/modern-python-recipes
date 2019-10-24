"""
Context manager for changing directory.
"""

from __future__ import annotations


import os

from pathlib import Path


class ChangeDir:
    """
    Provides context where the current working directory changes temporarily to
    destination. Afterwards, it returns to the previous current working
    (source).
    """
    def __init__(self, destination: str, source: str = '.') -> None:
        self._dst = self._sanitize_path(destination)
        self._src = self._sanitize_path(source)

    def __enter__(self) -> ChangeDir:
        os.chdir(self._dst)

        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        os.chdir(self._src)

    def __iter__(self):
        return self._dst.iterdir()

    def destination(self, as_posix=False):
        return self._dst if not as_posix else self._dst.as_posix()

    def source(self, as_posix=False):
        return self._src if not as_posix else self._src.as_posix()

    @staticmethod
    def _sanitize_path(target: str) -> Path:
        path = Path(target).resolve()

        if not path.exists():
            raise FileExistsError(f'Directory {path} does not exists')
        elif not (path.is_dir() or path.is_symlink()):
            raise ValueError(f'Item {path.name} is not a directory nor a '
                             'simbolic link')

        return path
