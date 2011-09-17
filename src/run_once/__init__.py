
# This file has mostly been done looking at the original PSF os.py

# Note:  more names are added to __all__ later.
__all__ = []

import sys

_names = sys.builtin_module_names

if 'posix' in _names:
    from posix import *
    import posix
    __all__.extend(list(posix.__all__))
    del(posix)

elif 'nt' in _names:
    from nt import *
    import nt
    __all__.extend(list(nt.__all__))
    del(nt)
