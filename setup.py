#!/usr/bin/python3
# vmmgr/setup.py

""" Set up distutils for vmmgr. """

import re
from distutils.core import setup
__version__ = re.search(r"__version__\s*=\s*'(.*)'",
                        open('src/vmmgr/__init__.py').read()).group(1)

# see http://docs.python.org/distutils/setupscript.html

setup(name='vmmgr',
      version=__version__,
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      py_modules=[],
      packages=['src/vmmgr'],
      # following could be in scripts/ subdir
      scripts=['src/vm_init', 'src/vm_kill', 'src/vm_launch',
               'src/vm_list', 'src/vm_scrub', 'src/vm_update', 
               'src/vm_verify', ],
      description='tools for managing VMs in EC2 cloud',
      url='https:/jddixon.github.io/vmmgr',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
