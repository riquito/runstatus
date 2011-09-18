#!/usr/bin/env python

from distutils.core import setup

setup(
    name = "runstatus",
    packages = ["runstatus"],
    version = __import__('runstatus').__version__,
    description = "a library to detect if a program is already running",
    author = "Riccardo Attilio Galli",
    author_email = "riccardo@sideralis.org",
    url = "https://github.com/riquito/runstatus/",
    keywords = ["process", "program", "run", "uptime"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    platforms = ['Windows','Mac OSX','Linux','BSD'],
    license = 'Apache Software License',
    long_description = file('README.rst').read()
)