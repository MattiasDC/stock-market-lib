import os
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name="stock-market-engine",
	  install_requires=required,
	  version="v0.1")