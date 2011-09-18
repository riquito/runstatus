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

import os,sys,atexit
from fcntl import lockf,LOCK_EX,LOCK_NB,LOCK_UN
from tempfile import gettempdir

from time import mktime,strptime
from datetime import date,datetime,timedelta

def get_system_start_time():
    """
    Retrieve system start time
    
    :return: unixtime
    :rtype: int
    """
    
    today = date.today()
    askTime,uptime = (x.strip() for x in os.popen('uptime').read().split(',')[0].split('up'))
    tsUptime = strptime(uptime,'%H:%M')
    tsAskTime = strptime(askTime,'%H:%M:%S')
    now = datetime(today.year,today.month,today.day) + timedelta(hours=tsAskTime.tm_hour,minutes=tsAskTime.tm_min)
    startTime = now - timedelta(hours=tsUptime.tm_hour,minutes=tsUptime.tm_min,seconds=tsUptime.tm_sec)
    return int(mktime(startTime.utctimetuple()))

def process_exists(pid,partial_name=''):
    """
    Check if a process is running
    
    :param pid: process id
    :type pid:  int
    :param partial_name: process' name (or part of it)
    :type partial_name:  string
    
    :return: whether the process is running
    :rtype: bool
    """
    
    pid = str(pid).strip()
    if not pid: return false
    pid = int(pid)
    
    # it would be faster to check for /proc/{pid} but osx doesn't support it
    process_string = os.popen('ps -p %d -o cmd=' % pid).read().strip()
    return bool(process_string and partial_name in process_string)

def process_kill(pid):
    """
    End the process identified by pid.
    
    :param pid: process id
    :type pid:  int
    """
    try:
      os.kill(int(pid),9) # send SIGKILL to pid
    except OSError as e:
      if e.errno == 3: # No such process
        pass
      else: raise e

def already_running(codeName):
    """
    Discover if the program is already running as another process
    
    :param codeName: a unique name given to the current program
    :type codeName:  string
    
    :return: whether the program is already running as a different process
    :rtype:  boolean
    """
    
    pathLockFile = os.path.join(gettempdir(),'lock_'+codeName)
    
    fd = os.open(pathLockFile,os.O_RDWR|os.O_CREAT)
    fp = os.fdopen(fd,'r+')
    
    isSingle = False
    
    try:
        lockf(fp,LOCK_EX|LOCK_NB)
        line = fp.read()
        
        pid = ''
        if line:
           pid, pidSysStartTime = (int(x) for x in line.split())

        sysStartTime = get_system_start_time()
        
        isSingle = not (pid and sysStartTime == pidSysStartTime and process_exists(pid))
        
        if isSingle:
            # app is not running, update the content of the lock file
            fp.seek(0)
            fp.write('%d %d' % (os.getpid(),sysStartTime))
            fp.truncate()
            atexit.register(os.remove,pathLockFile)
        
        lockf(fp,LOCK_UN)
        fp.close()
    
    except IOError as e:
        if e.errno == 11: # Resource temporarily unavailable 
           pass           # (failed to lock because we're not alone)
        else: raise e
    finally:
        try: fp.close()
        except: pass
    
    return isSingle
    

