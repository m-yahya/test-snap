# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# The current directory
with open("README.md", "r") as f:
    README = f.read()

setup(name='olibox-core',
      version='0.1dev',
      description='The package provided core functionality for oli box',
      long_description=README,
      long_description_content_type="text/markdown",
      author='Muhammad Yahya & Felix Forster @ OLI Systems 2020',
      url='https://github.com/olisystems/olibox_core',
      packages=['olibox_core.olibox_core.olibox_pkg', 'olibox_core.olibox_core.core_modules',
                'olibox_core.olibox_core'],
      install_requires=['click', 'toml', 'datetime', 'pymodbus',
                        'RPi.GPIO', 'paho-mqtt', ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent", ],
      entry_points={
          'console_scripts': [
              'olibox-core = olibox_core.olibox_core.olibox_core:init'
          ]
      },
      )
