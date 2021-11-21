from setuptools import find_packages, setup

setup(
    name="repocutter",
    version="0.0.1",
    description="Repocutter",
    author="Jordi Smit",
    author_email="jordismit2000@gmail.com",
    url="https://github.com/j0rd1smit/repocutter",
    license="MIT",
    packages=["repocutter"],
    install_requires=[
        "prompt-toolkit>=3.0.22",
        "requests>=2.26.0",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "repocutter=repocutter:main",
        ],
    },
)
