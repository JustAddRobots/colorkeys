#!/usr/bin/env python3

"""
This module facilitates the creating image histogram data.

    Typical Usage:

    my_histogram = Hist(img, "kmeans", 5, "RGB", "720")
"""

import cv2
import logging
import numpy as np
import operator

from skimage import color as skicolor
from skimage import util as skiutil
from colorkeys.centroids import Clust

logger = logging.getLogger(__name__)


class Hist(Clust):
    """A class for generating histogram and histogram bar information based on
    input clusters. In other words, this generates the color palette bar.

    Attributes:
        hist (numpy.ndarray): Normalized histogram of centroids.
        colorspace (str): Histogram color space
        hist_bar (numpy.ndarray): Normalized histogram bar scaled to image width.
        hist_bar_height (int): histogram bar height.
    """
    def __init__(self, img, algo, num_clusters, colorspace, render_width):
        """Init Hist.

        Args:
            img (np.ndarray): Image array.
            algo (str): Clustering algorithm requested.
            num_clusters (int): Requested Number of clusters/centroids.
            colorspace (str): Requested color space of histogram.
            render_width (int): Width of image (used to define width for histogram bar).
        """
        self._algo = self._get_algo(algo)
        self._colorspace = self._get_colorspace(colorspace)
        img = self._preprocess(img)
        super().__init__(img, algo, num_clusters)

        self._hist_bar_height = 30
        self._hist = self._get_hist()
        self._hist_bar = self._get_hist_bar(render_width)

    @property
    def hist(self):
        """Get histogram."""
        return self._hist

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
        if algo not in ("kmeans", "hac"):
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

    def _get_hist_bar(self, render_width):
        """Get histogram bar from histogram.

        Generate a histogram bar using centroids. The sklearn.cluster generated
        centroids (cluster centers) are coordinates in the image. Use the color
        at each centroid to generate a bar based on relative percentage (scaled
        by image width) that the centroid occupies in the normalised histogram.

        Args:
            render_width (int): Width of rescaled image, used for histogram bar width.

        Returns:
            hist_bar (numpy.ndarray): Histogram bar.
        """
        num_channels = 3
        # Start with zeroed histogram.
        hist_bar = np.zeros(
            (self._hist_bar_height, render_width, num_channels),
            dtype = "uint8",
        )

        # Convert cluster to RGB.
        if self._colorspace == "HSV":
            cents = skicolor.hsv2rgb(self.centroids)
        elif self._colorspace == "RGB":
            cents = self.centroids
        else:
            raise ValueError(f"Invalid colorspace, {self._colorspace}")

        # Sort centroids descending by percentage.
        zipped = zip(self._hist, cents)
        centroids_sorted = sorted(zipped, key=operator.itemgetter(0), reverse=True)

        # Build the bar each centroid color at a time.
        start_x = 0
        for (percent, color) in centroids_sorted:
            end_x = start_x + (percent * render_width)
            cv2.rectangle(
                hist_bar,
                (int(start_x), 0),
                (int(end_x), self._hist_bar_height),
                skiutil.img_as_ubyte(color).tolist(),
                -1,
            )
            start_x = end_x
        return hist_bar
