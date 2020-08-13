#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# Filename: setup.py
# Author: Ming Zhao
# Mail: mingzhao@microsoft.com
# Created Time:  2020-08-12
#############################################

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="codelet",
    version="1.0.2",
    description="Codelet for Engineer Excellence",
    license="MIT Licence",
    url="https://github.com/Azure",
    author="Ming Zhao",
    author_email="mingzhao@microsoft.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
	packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
	install_requires=[
		'pyperclip',
    ],
	include_package_data=True,
    zip_safe=False,
    platforms="any"
)