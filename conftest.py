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
    return cli.get_command(shlex.split("-d -n 5 -i {0}".format(testimg)))


@pytest.fixture(scope="session")
def myartwork():
    return Artwork(testimg)


@pytest.fixture(scope="session")
def myclust():
    a = Artwork(testimg)
    return Clust(a.img, "kmeans", 5)


@pytest.fixture(scope="session")
def myhist():
    a = Artwork(testimg)
    return Hist(a.img, "kmeans", 5, a.img_width)


@pytest.fixture(scope="session")
def mycolorkey():
    return ColorKey(testimg, ["kmeans"], 5)
