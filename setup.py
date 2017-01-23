# -*- coding: utf-8 -*-
from setuptools import setup

requirements = [
    'requests>=2.10.0',
    'beautifulsoup4>=4.4.1'
]

setup(
  name = 'bibliothequetoulouse',
  packages = ['bibliothequetoulouse'],
  version = '0.1.1',
  license='MIT',
  platforms='Posix; MacOS X',
  description = 'Package pour interroger le catalogue des bibliothèques de Toulouse',
  author = 'Thibault Ducret',
  author_email = 'thibault.ducret@gmail.com',
  url = 'https://github.com/thibdct/bibliotheque-toulouse-python',
  download_url = 'https://github.com/thibdct/bibliotheque-toulouse-python/tarball/0.1.1', # I'll explain this in a second
  keywords = ['api', 'bibliothèque', 'toulouse'],
  setup_requires=requirements,
  install_requires=requirements,
  classifiers = ['Programming Language :: Python :: 2.7'],
)