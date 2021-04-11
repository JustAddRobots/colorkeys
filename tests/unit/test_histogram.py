#!/usr/bin/env python3

import numpy as np


def test_num_clusters(myhist):
    assert myhist.num_clusters == 5


def test_hist(myhist):
    assert isinstance(myhist.hist, np.ndarray)


def test_hist_colorspace(myhist):
    assert myhist.colorspace == "RGB"


def test_hist_bar(myhist):
    assert isinstance(myhist.hist_bar, np.ndarray)


def test_hist_bar_height(myhist):
    assert myhist.hist_bar_height == 30
