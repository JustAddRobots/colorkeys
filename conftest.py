#!/usr/bin/env python3

import pytest
import shlex

from colorkeys.artwork import Artwork
from colorkeys.centroids import Clust
from colorkeys import cli
from colorkeys.histogram import Hist
from colorkeys.colorkeys import ColorKey

collect_ignore = ["setup.py"]
testimg = "tests/fixture-01.png"


@pytest.fixture(scope="session")
def myargs():
    return cli.get_command(shlex.split("-d -n 5 -i {0} -i {0}".format(testimg)))


@pytest.fixture(scope="session")
def myimagepaths():
    return [
        ["tests"],
        ["tests/*.png"],
        ["tests/fixture*"],
        ["tests/fixture-01.jpg"],
        [(
            "https://upload.wikimedia.org/wikipedia/"
            "commons/thumb/b/b4/Vincent_Willem_van_Gogh_128.jpg/"
            "192px-Vincent_Willem_van_Gogh_128.jpg"
        )],
    ]


@pytest.fixture(scope="session")
def myimagepaths_shell_glob():
    return [
        ["tests/fixture-01.jpg", "tests/fixture-01.png"]
    ]


@pytest.fixture(scope="session")
def myartwork():
    return Artwork(testimg)


@pytest.fixture(scope="session")
def myclust():
    a = Artwork(testimg)
    return Clust(a.img, "mbkmeans", 5)


@pytest.fixture(scope="session")
def myhist():
    a = Artwork(testimg)
    return Hist(a.img, "mbkmeans", 5, "RGB", a.img_width)


@pytest.fixture(scope="session")
def mycolorkey():
    return ColorKey(testimg, "mbkmeans", 5, colorspace="RGB")
