# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

PACKAGE = 'argcheck'
NAME = 'argcheck'
VERSION = '0.0.2'
DESCRIPTION = 'Argument check decorator'
AUTHOR = 'iLampard'
URL = 'https://github.com/iLampard/argcheck'
LICENSE = 'Apache 2.0'

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      url=URL,
      packages=find_packages(),
      install_requires=[
          'pandas',
          'numpy',
          'toolz',
      ],
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5'])
