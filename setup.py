# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
from setuptools import setup, find_packages

with open("python/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aswfdocker",
    version="0.2.0",
    author="Aloys Baillet",
    author_email="aloys.baillet+github@gmail.com",
    description="ASWF Docker Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AcademySoftwareFoundation/aswf-docker",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2 License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "certifi==2020.4.5.1",
        "chardet==3.0.4",
        "click==7.1.2",
        "deprecated==1.2.10",
        "idna==2.9",
        "pygithub==1.51",
        "pyjwt==1.7.1",
        "pyyaml==5.3.1",
        "requests==2.23.0",
        "urllib3==1.25.9",
        "wrapt==1.12.1",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["aswfdocker=aswfdocker.cli.aswfdocker:cli",],},
)
