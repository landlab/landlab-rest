#! /usr/bin/env python
from setuptools import find_packages, setup

import versioneer


setup(
    name="landlab_rest",
    version=versioneer.get_version(),
    author="Eric Hutton",
    author_email="eric.hutton@colorado.edu",
    description="A RESTful interface to landlab graphs.",
    long_description=open("README.rst").read(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=["flask", "cherrypy", "landlab", "xarray"],
    packages=find_packages(),
    cmdclass=versioneer.get_cmdclass(),
    entry_points={"console_scripts": ["start-landlab-sketchbook=landlab_rest.run:main"]},
)
