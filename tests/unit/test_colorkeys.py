#!/usr/bin/env python3

import colorkeys


def test_hists(mycolorkey):
    assert isinstance(mycolorkey.hists, dict)


def test_hist(mycolorkey):
    assert isinstance(mycolorkey.hists["kmeans"], colorkeys.histogram.Hist)
