import os
from setuptools import setup, find_packages

requirements_path = './requirements.txt'
install_requires = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()

setup(name='stock-market-engine', version='0.1', install_requires=install_requires, packages=find_packages())