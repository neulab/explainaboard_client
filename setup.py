from setuptools import setup, find_packages
import codecs
from version import __version__
import os

setup(
    name="explainaboard",
    version=__version__,
    description="Explainable CLI",
    long_description=codecs.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ExpressAI/ExplainaBoard",
    license="MIT License",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Text Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
        ],
    },
    install_requires=[],
    include_package_data=True,
)
os.system("pip install https://github.com/neulab/explainaboard_web/releases/download/latest/explainaboard_api_client-1.0.0-py3-none-any.whl")
