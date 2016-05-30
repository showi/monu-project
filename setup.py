#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import monu as app


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requires = [];
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    requires = f.read().strip().split('\n')
print('req: %s' % requires)
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

packages = [
    'monu',
]

package_data = {
}


classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask, SqlAlchemy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Web Service :: Temporary files',
        'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='monu',
    version=app.__version__,
    description='',
    long_description=readme,
    packages=packages,
    package_data=package_data,
    install_requires=requires,
    author=app.__author__,
    author_email=app.__email__,
    url='',
    license='MIT',
    classifiers=classifiers,
)
