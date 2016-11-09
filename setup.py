#!/usr/bin/env python
import sys
from setuptools import setup


install_requires = ['aiohttp>=1.1.1']


setup(name='aiohttp_healthcheck',
      version='1.3.1',
      description='Adds healthcheck endpoints to aiohttp apps. Based on https://github.com/Runscope/healthcheck.',
      author='Frank Stratton',
      author_email='frank@runscope.com',
      maintainer='Brannon Jones',
      maintainer_email='brannonj@gmail.com',
      url='https://github.com/brannon/aiohttp-healthcheck',
      packages=['aiohttp_healthcheck'],
      zip_safe=True,
      license='MIT',
      platforms='any',
#      python_requires='>=3.4.2',
      install_requires=install_requires,
      classifiers=('Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5'))
