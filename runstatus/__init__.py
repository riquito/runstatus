
__version__ = "1.0"
__all__ = ['get_system_start_time','process_exists','process_kill','already_running']

import sys

_names = sys.builtin_module_names

if 'posix' in _names:
    from .posix import *

elif 'nt' in _names:
    from .nt import *
