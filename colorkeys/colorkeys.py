#!/usr/bin/env python3

"""
This module creates and displays color keys (palettes) from a requested image.

    Typical Usage:

    my_colorkey = ColorKey("my_image_file.png", ["kmeans"], 5, colorspace="RGB")
"""

import logging

from colorkeys.artwork import Artwork
from colorkeys.histogram import Hist

logger = logging.getLogger(__name__)


class ColorKey(Artwork):
    """A class for loading, generating, and displaying image color keys.

    Each instance has a "hist" dict that includes color palette values
    (histogram, histogram bar, etc.) for each combination of clustering
    algorithm + colorspace.

    Attributes:
        hist (colorkeys.histogram.Hist): Histogram information.
    """
    def __init__(self, imgsrc, algo, num_clusters, **kwargs):
        super().__init__(imgsrc, **kwargs)
        """Init ColorKey.

        The number of color keys (palettes) generated for each image:
            len(algos) * len(colorspaces).

        Args:
            imgsrc (str): Image source location.
            algos (list): Algorithms requested.
            num_clusters (int): Number of clusters requested.

        kwargs:
            colorspace (str): Colorspace for which to generate histogram information.
        """
        self._hist_colorspace = kwargs["colorspace"]
        self._hist = self._get_hist(algo, num_clusters)

    @property
    def hist(self):
        return self._hist

    def _get_hist(self, algo, num_clusters):
        """Get histogram information for the algorithm requested.

        Args:
            algo (str): Algorithm requested.
            num_clusters (int): Number of clusters requested.

        Returns:
            hist (colorkeys.histogram.Hist): Histogram information.
        """
        hist = Hist(
            self.img,
            algo,
            num_clusters,
            self._hist_colorspace,
            self.rescaled_width,
        )
        return hist
