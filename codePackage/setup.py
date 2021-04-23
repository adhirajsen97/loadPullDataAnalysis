#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#Change the first line to '#!/usr/bin/env python' if python 3 is installed as python
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loadPullDataAnalysis",
    version="1.2.6",
    author="Rutvij Shah",
    author_email="rutvij.shah96@gmail.com",
    description="A package to perform load pull data analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xrutvij/LP_S21_AAHRS",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
