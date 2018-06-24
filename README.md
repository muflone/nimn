New in my net [![Build Status](https://travis-ci.org/muflone/nimn.svg?branch=master)](https://travis-ci.org/muflone/nimn)
=====

**Description:** Find new devices in my network.

**Copyright:** 2018 Fabio Castelli (Muflone) <muflone(at)vbsimple.net>

**License:** GPL-2+

**Source code:** https://github.com/muflone/nimn

**Documentation:** http://www.muflone.com/nimn/

System Requirements
-------------------

* Python 2.x (developed and tested for Python 2.7.5)
* XDG library for Python 2.x
* Distutils library for Python 2.x (usually shipped with Python distribution)

External tools:

* ping (with NET capabilities)
* arping (with NET capabilities)

Installation
------------

A distutils installation script is available to install from the sources.

To install in your system please use:

    cd /path/to/folder
    python2 setup.py install

To install the files in another path instead of the standard /usr prefix use:

    cd /path/to/folder
    python2 setup.py install --root NEW_PATH

Usage
-----

If the application is not installed please use:

    cd /path/to/folder
    python2 nimn.py

If the application was installed simply use the nimn command.
