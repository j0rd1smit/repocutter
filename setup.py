#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="repocutter",
    version="0.0",
    description="Repocutter",
    author="Jordi Smit",
    author_email="jordismit2000@gmail.com",
    url="https://github.com/j0rd1smit/repocutter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "prompt-toolkit>=3.0.22",
        "requests>=2.26.0",
    ],
    entry_points={
        "console_scripts": [
            "repocutter=repocutter",
        ],
    },
)
