import codecs

from setuptools import find_packages, setup
from version import __version__

setup(
    name="explainaboard_client",
    version=__version__,
    description="ExplainaBoard Client",
    long_description=codecs.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/neulab/explainaboard_client",
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
    install_requires=["explainaboard_api_client>=0.1.3", "tqdm"],
    extras_require={
        "dev": [
            "pre-commit",
        ],
    },
    include_package_data=True,
)
