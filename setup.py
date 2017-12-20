#!/usr/bin/python3
# vmmgr/setup.py

""" Setuptools project configuration for vmmgr. """

from os.path import exists
from setuptools import setup

LONG_DESC = None
if exists('README.md'):
    with open('README.md', 'r') as file:
        LONG_DESC = file.read()

setup(name='vmmgr',
      version='0.5.20',
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      long_description=LONG_DESC,
      packages=['vmmgr'],
      package_dir={'': 'src'},
      py_modules=[],
      include_package_data=False,
      zip_safe=False,
      scripts=['src/vm_init', 'src/vm_kill', 'src/vm_launch', 'src/vm_list',
               'src/vm_scrub', 'src/vm_update', 'src/vm_verify'],
      ext_modules=[],
      description='tools for managing VMs in EC2 cloud',
      url='https://jddixon.github.io/vmmgr',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 2.7',
          'Programming Language :: Python 3.3',
          'Programming Language :: Python 3.4',
          'Programming Language :: Python 3.5',
          'Programming Language :: Python 3.6',
          'Programming Language :: Python 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
