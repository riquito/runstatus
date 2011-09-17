
# This file has mostly been done looking at the original PSF os.py

# Note:  more names are added to __all__ later.
__all__ = []

import sys

_names = sys.builtin_module_names

def _get_exports_list(module):
    try:
        return list(module.__all__)
    except AttributeError:
        return [n for n in dir(module) if n[0] != '_']

if 'posix' in _names:
    from posix import *
    import posix
    __all__.extend(_get_exports_list(posix))
    del posix

elif 'nt' in _names:
    from nt import *
    import nt
    __all__.extend(_get_exports_list(nt))
    del nt
