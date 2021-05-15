#!/usr/bin/env python3

import colorkeys


def test_hist(mycolorkey):
    assert isinstance(mycolorkey.hist, colorkeys.histogram.Hist)
