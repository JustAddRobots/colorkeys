#!/usr/bin/env python3

import numpy as np


def test_filename(myartwork):
    assert myartwork.imgsrc == "tests/fixture-01.png"


def test_colorspace(myartwork):
    assert myartwork.img_colorspace == "RGB"


def test_img(myartwork):
    assert isinstance(myartwork.img, np.ndarray)


def test_img_height(myartwork):
    assert myartwork.img_height == 100


def test_img_width(myartwork):
    assert myartwork.img_width == 100


def test_num_channels(myartwork):
    assert myartwork.num_channels == 3
