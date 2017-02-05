# -*- coding: utf-8 -*-
from setuptools import setup
from pip.req import parse_requirements

_VERSION = '0.1.3'
install_reqs = parse_requirements('requirements.txt', session='hack')
requirements = [str(ir.req) for ir in install_reqs]

setup(
  name = 'bibliothequetoulouse',
  packages = ['bibliothequetoulouse'],
  version = _VERSION,
  license='MIT',
  platforms='Posix; MacOS X',
  description = 'Package pour interroger le catalogue des bibliothèques de Toulouse',
  author = 'Thibault Ducret',
  author_email = 'thibault.ducret@gmail.com',
  url = 'https://github.com/thibdct/bibliotheque-toulouse-python',
  download_url = 'https://github.com/thibdct/bibliotheque-toulouse-python/tarball/%s' % (_VERSION), # I'll explain this in a second
  keywords = ['api', 'bibliothèque', 'toulouse'],
  setup_requires=requirements,
  install_requires=requirements,
  classifiers = ['Programming Language :: Python :: 2.7'],
  tests_require=['pytest'],
)