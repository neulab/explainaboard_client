import codecs
import os

from setuptools import find_packages, setup

from version import __api_client_version__, __version__

setup(
    name="explainaboard_cli",
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [],
    },
    install_requires=[],
    extras_require={
        "dev": [
            "pre-commit",
        ],
    },
    include_package_data=True,
)
os.system(
    "pip install https://github.com/neulab/explainaboard_web/releases"
    f"/download/{__api_client_version__}"
    "/explainaboard_api_client-1.0.0-py3-none-any.whl"
)
