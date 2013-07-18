#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from distutils.core import setup
try:
    import py2exe
    py2exe_avail = True
except:
    py2exe_avail = False

setup_args = {'name': 'pysimm',
      'version': '0.1.0',
      'author': u'Dominique Cyprès',
      'author_email': 'lunasspecto@gmail.com',
      'url': 'http://lunasspecto.github.io/pysimm',
      'license': 'This software released under the GNU Public License (GPL)',
      'description': 'Z-code interpreter implemented in Python.',
      'requires': ['Tkinter', 'tkFileDialog', 'tkMessageBox', 'pyglet'],
      'scripts': ['zverify'],
      'packages': ['pysimm'],
      'package_dir': {'pysimm': 'lib'},
      'classifiers': ['License :: OSI Approved :: \
                       GNU General Public License (GPL)',
                      'Topic :: Games/Entertainment',
                      'Operating System :: OS Independent',
                      'Programming Language :: Python :: 2',
                      'Development Status :: 2 - Pre-Alpha',
                      'Intended Audience :: End Users/Desktop']}

if sys.version < '2.2.3':
    del setup_args['classifiers']

if py2exe_avail:
    setup_args['windows'] = ['zverify']

setup(**setup_args)
