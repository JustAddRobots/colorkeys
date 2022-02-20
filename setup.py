import os
from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


with open(os.path.dirname(__file__) + "/VERSION") as f:
    pkgversion = f.read().strip()


if 'ENGCOMMON_BRANCH' in os.environ:
    engcommon_branch = os.getenv("ENGCOMMON_BRANCH")
else:
    engcommon_branch = "main"


setup(
    name = "colorkeys",
    version = pkgversion,
    description = "Color Key and Palette Analysis in Art and Film",
    url = "https://github.com/JustAddRobots/colorkeys",
    author = "Roderick Constance",
    author_email = "justaddrobots@icloud.com",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    license = "GPLv3",
    python_requires = ">=3.6",
    packages = [
        "colorkeys",
    ],
    install_requires = [
        (
            f"engcommon @ "
            f"git+https://github.com/JustAddRobots/engcommon.git@{engcommon_branch}"
        ),
        "boto3",
        "ffmpeg-python",
        "matplotlib",
        "numpy",
        "scikit-image",
        "scikit-learn",
    ],
    entry_points = {
        "console_scripts": [
            "colorkeys = colorkeys.cli:main",
            "colordb = colorkeys.colordb:main",
        ]
    },
    zip_safe = False
)
