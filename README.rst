runstatus - library to detect if a program is already running
=============================================================

Knowing if a program is already running can be useful to avoid doing
concurrently operations that should always be serialized, or augment
the usability of a software so that the user do not end up having 
multiple instances of the same program open at once.

All of this in a cross-platform way.

The library is trivial to use

    import runstatus

    if runstatus.already_running('myAppName'):
        print('do something, e.g. exiting')
        exit(0)

The library comes with some additional functions

* ``get_system_start_time()`` will give you the time when the computer
  was turned on in unixtime

* ``process_exists(pid)`` will tell you if a process with that id is
  running

* ``process_kill(pid)`` will kill the process with that id if exists

Install
-------

Either use ``pip install runstatus`` or download the sources and run
``python setup.py install``. No dependencies are required. Run on
python 2.7 or 3.x

Download
--------

The git repository is available at https://github.com/riquito/runstatus

Copyright and License
---------------------

runstatus was developed by Riccardo Attilio Galli <riccardo@sideralis.org>
and is licensed under the Apache License (see LICENSE file)

Website
-------
http://www.sideralis.org
