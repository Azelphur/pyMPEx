#!/usr/bin/python
"""
A simple setup script for pyMPEx.

Created on Wed Aug  1 17:15:09 2012

@author: Michael 'smickles' Carver

Copyright 2012 Michael 'smickles' Carver

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from distutils.core import setup

setup(name='pyMPEx',
      version='1.0',
      description='A command line frontend and library for communication ' +
                  'with MPEx.',
      author='Azelphur',
      author_email='support@azelphur.com',
      url='https://github.com/Azelphur/pyMPEx',
      py_modules=['mpex'],
      requires=['gnupg'])