# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 09:28:49 2020

@author: luc_e
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SLiCAP_python", # Replace with your own username
    version="0.9.0",
    author="Anton Montagne",
    author_email="anton@montagne.nl",
    description="Symbolic Linear Circuit Analysis Program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lenty/SLiCAP_python/",
    packages=setuptools.find_packages(),
    # py_modules = ['src.SLiCAP', 'src.SLiCAPnotebook'],
    #packages=['SLiCAP'],
    #package_dir={'SLiCAP': 'SLiCAP'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Attribution-NonCommercial-NoDerivatives 4.0 International",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)