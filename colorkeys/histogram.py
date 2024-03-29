#!/usr/bin/env python3

"""
This module facilitates the creating image histogram data.

    Typical Usage:

    my_histogram = Hist(img, "kmeans", 5, "RGB", 720)
"""

import logging
import numpy as np

from operator import itemgetter
from skimage import color as skicolor
from skimage import draw as skidraw
from skimage import util as skiutil

from colorkeys.centroids import Clust
from colorkeys.constants import _const as CONSTANTS

logger = logging.getLogger(__name__)


class Hist(Clust):
    """A class for generating histogram and histogram bar information based on
    input clusters. In other words, this generates the color palette bar.

    Attributes:
        hist (numpy.ndarray): Normalized histogram of centroids.
        hist_centroids (dict): RGB values ([R,G,B]) by normalised percentage.
        colorspace (str): Histogram color space.
        hist_bar (numpy.ndarray): Normalized histogram bar scaled to image width.
        hist_bar_height (int): Histogram bar height.
    """
    def __init__(self, img, algo, num_clusters, colorspace, rescaled_width):
        """Init Hist.

        Args:
            img (np.ndarray): Image array.
            algo (str): Clustering algorithm requested.
            num_clusters (int): Requested Number of clusters/centroids.
            colorspace (str): Requested color space of histogram.
            rescaled_width (int): Width of image (defines width for histogram bar).
        """
        self._algo = self._get_algo(algo)
        self._colorspace = self._get_colorspace(colorspace)
        img = self._preprocess(img)
        super().__init__(img, algo, num_clusters)

        self._hist_bar_height = CONSTANTS().HIST_BAR_HEIGHT
        self._hist = self._get_hist()
        self._hist_centroids = self._get_hist_centroids()
        self._hist_bar = get_hist_bar(
            self._hist_centroids,
            height = self._hist_bar_height,
            width = rescaled_width
        )

    @property
    def hist(self):
        """Get histogram."""
        return self._hist

    @property
    def hist_centroids(self):
        """Get histogram and centroids."""
        return self._hist_centroids

    @property
    def algo(self):
        """Get histogram algorithm."""
        return self._algo

    @property
    def colorspace(self):
        """Get histogram color space."""
        return self._colorspace

    @property
    def hist_bar(self):
        """Get histogram bar."""
        return self._hist_bar

    @property
    def hist_bar_height(self):
        """Get histogram bar."""
        return self._hist_bar_height

    def _get_algo(self, algo):
        """Get algorithm."""
        if algo not in ("kmeans", "mbkmeans", "hac"):
            raise ValueError(f"Invalid algorithm, {algo}")
        return algo

    def _get_colorspace(self, colorspace):
        """Get colorspace."""
        if colorspace not in ("RGB", "HSV"):
            raise ValueError(f"Invalid colorspace, {colorspace}")
        return colorspace

    def _preprocess(self, img):
        """Prepare image array for processing.

        Convert to float for better precision, convert to the color space of histogram.

        Args:
            img (np.ndarray): Image array.

        Returns:
            img (np.ndarray): Image array.

        Raises:
            ValueError: colorspace not valid.
        """
        img = skiutil.img_as_float(img)
        if self._colorspace == "HSV":
            img = skicolor.rgb2hsv(img)
        elif self._colorspace == "RGB":
            pass  # default
        else:
            raise ValueError(f"Invalid colorspace, {self._colorspace}")
        return img

    def _get_hist(self):
        """Get histogram from generated cluster.

        The sklearn.cluster is an array of labels. The clustering algorithm assigns
        a cluster label to each point. A histogram is generated by separating
        these labels into bins. The resulting histogram is then normalised to 1.

        Args:
            None

        Returns:
            hist (numpy.ndarray): Normalized histogram.
        """
        num_labels = np.arange(0, len(np.unique(self.clust.labels_)) + 1)
        (hist, _) = np.histogram(self.clust.labels_, bins=num_labels)
        hist = skiutil.img_as_float(hist)
        hist /= hist.sum()
        return hist

    def _get_hist_centroids(self):
        """Get centroid RGB values by percentage in descending order.

        Args:
            None

        Returns:
            hist_cents (dict): RGB values ([R,G,B]) keyed by percentage.

        Raises:
            ValueError: colorspace not valid.
        """
        # Convert centroids to RGB.
        if self._colorspace == "HSV":
            cents = skicolor.hsv2rgb(self.centroids)
        elif self._colorspace == "RGB":
            cents = self.centroids
        else:
            raise ValueError(f"Invalid colorspace, {self._colorspace}")

        # Sort centroids descending by percentage.
        listcomp = [
            {
                "percent": i,
                "color": skiutil.img_as_ubyte(v).tolist()
            } for i, v in zip(self._hist, cents)
        ]
        hist_cents = sorted(listcomp, key=itemgetter("percent"), reverse=True)
        return hist_cents


def get_hist_bar(hist_centroids, height, width):
    """Get histogram bar from histogram.

    Generate a histogram bar using percentage and RGB values. The
    sklearn.cluster-generated centroids (cluster centers) are RGB color values.
    Use these colors to generate a bar based on relative percentage (scaled by
    image width) that the centroid occupies in the normalised histogram.

    Args:
        hist_centroids (list): Dictionaries with keys "color" for RGB values ([R,G,B])
            and "percent" for normalised percentage which the color occupies.
        height (int): Height of histogram bar.
        width (int): Width of histogram bar.

    Returns:
        hist_bar (numpy.ndarray): Histogram bar.

    Ex: get_hist_bar([
        {"percent": 0.5, "color": [255,255,255]},
        {"percent": 0.3, "color": [127,127,127]},
        {"percent": 0.2, "color": [0,0,0]}
    ], 50, 1000)
    Will generate a 50x1000 px histogram bar that is 50% white, 30% grey, 20% black.
    """
    num_channels = 3
    # Start with zeroed histogram.
    hist_bar = np.zeros(
        (height, width, num_channels),
        dtype = "uint8",
    )

    # Build the bar each centroid color at a time.
    start_x = 0
    for i in hist_centroids:
        end_x = start_x + (i["percent"] * width)
        rr, cc = skidraw.rectangle(
            (0, int(start_x)),
            (height, int(end_x)),
            shape = hist_bar.shape,
        )
        skidraw.set_color(hist_bar, (rr, cc), i["color"])
        start_x = end_x
    return hist_bar
