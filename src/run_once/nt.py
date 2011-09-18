#!/usr/bin/env python

'''
Copyright 2011 Riccardo Attilio Galli <riccardo@sideralis.org> [http://www.sideralis.org]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

__all__ = ['get_system_start_time','process_exists','process_kill','already_running']

import os
from time import mktime,strptime
from datetime import date,datetime,timedelta
import ctypes


def get_system_start_time():
    """
    Retrieve system start time
    
    :return: unixtime
    :rtype: int
    """
    
    output = os.popen('wmic os get lastbootuptime').read()
    startTimeString = output.split()[1].split('.')[0]
    return int(mktime(strptime(startTimeString,'%Y%m%d%H%M%S')))


def process_exists(pid,partial_name=''):
    """
    Check if a process is running
    
    Note, in nt systems partial_name is ignored
    
    :param pid: process id
    :type pid:  int
    :param partial_name: process' name (or part of it)
    :type partial_name:  string
    
    :return: whether the process is running
    :rtype: bool
    """
    
    return 3 == len(os.popen('tasklist /FI "pid eq %s"' % pid).read().strip().splitlines())


def process_kill(pid):
    """
    End the process identified by pid.
    
    :param pid: process id
    :type pid:  int
    """
    if pid_exists(pid):
        os.system('taskkill /pid %s' % pid)



# Microsoft Constants
INVALID_HANDLE_VALUE = -1
ERROR_ALREADY_EXISTS = 183
WAIT_FAILED = 0xFFFFFFFF
WAIT_OBJECT_0 = 0x00000000L
WAIT_ABANDONED = 0x00000080L
INFINITE = 0xFFFFFFFF

kerneldll = ctypes.windll.kernel32
_create_mutex = kerneldll.CreateMutexA
_close_handle = kerneldll.CloseHandle
_get_last_error = kerneldll.GetLastError
_wait_for_single_object = kerneldll.WaitForSingleObject

def already_running(codeName):
    """
    Discover if the program is already running as another process
    
    :param codeName: a unique name given to the current program
    :type codeName:  string
    
    :return: whether the program is already running as a different process
    :rtype:  boolean
    """
    
    isSingle = False
    
    handle = _create_mutex(None, True, codeName)
    
    if handle != INVALID_HANDLE_VALUE:
        if _get_last_error() != ERROR_ALREADY_EXISTS:
            isSingle = True
        else:
            val = _wait_for_single_object(handle, 0)
            
            # If the mutex is signaled, or abandoned release it
            # If it was abandoned, it will become normal now
            isSingle = (val == WAIT_OBJECT_0) or (val == WAIT_ABANDONED)
    
    return isSingle


