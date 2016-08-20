# -*- coding: utf-8 -*-

from os.path import dirname, join

from setuptools import setup, find_packages

project_dir = dirname(__file__)

with open(join(project_dir, 'VERSION'), 'r') as f:
    version = f.read().strip()

setup(
    name="configreset",
    version=version,
    description="configreset",
    author="lvjiyong",
    url="https://github.com/lvjiyong/configreset",
    license="GPL",
    include_package_data=True,
    packages=find_packages(exclude=()),
    long_description=open(join(project_dir, 'README'), 'r').read(),
    maintainer='lvjiyong',
    platforms=["any"],
    maintainer_email='lvjiyong@gmail.com',
    install_requires=['six'],
)