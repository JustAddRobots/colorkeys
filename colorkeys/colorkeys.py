#!/usr/bin/env python3

"""
This module creates and displays color keys (palettes) from a requested image.

    Typical Usage:

    my_colorkey = ColorKey("my_image_file.png", ["kmeans"], 5)
    my_colorkey.show_palettes()
"""

import logging
import os.path

from urllib.parse import urlparse

from colorkeys.artwork import Artwork
from colorkeys.constants import _const as CONSTANTS
from colorkeys.histogram import Hist

logger = logging.getLogger(__name__)


class ColorKey(Artwork):
    """A class for loading, generating, and displaying image color keys.

    Each instance has a "hist" dict that includes color palette values
    (histogram, histogram bar, etc.) for each combination of clustering
    algorithm + colorspace.

    Attributes:
        hists (dict): colorkeys.histogram.Hist(s), key is "{algo}_{colorspace}"
        show_palettes (None): Display image(s) and palette(s).
    """
    def __init__(self, imgsrc, algo, num_clusters, **kwargs):
        super().__init__(imgsrc, **kwargs)
        """Init ColorKey.

        The number of color keys (palettes) generated for each image:
            len(algos) * len(colorspaces).

        Args:
            imgsrc (str): Image source location.
            num_clusters (int): Number of clusters requested.
            algos (list): Algorithms requested.
        """
        self._hist = self._get_hist(algo, num_clusters)
        self._figure_size = CONSTANTS().FIGURE_SIZE
        if self.imgsrc.startswith(("http://", "https://")):
            u = urlparse(self.imgsrc)
            self._figure_name = u.path.split("/")[-1]
        else:
            self._figure_name = os.path.basename(self.imgsrc)

    @property
    def hist(self):
        return self._hist

    def show_palettes(self):
        return self._show_palettes()

    def _get_hist(self, algo, num_clusters):
        """Get histogram information for the algorithm requested.

        Args:
            num_clusters (int): Number of clusters requested.
            algo (str): Algorithm requested.

        Returns:
            hist (dict): colorkeys.histogram.Hist object keyed by algorithm
                and colorspace combined {algo}_{colorspace} string.
            Ex:
                hist["kmeans_RGB"] = colorkeys.histogram.Hist
        """
        hist = Hist(
            self.img,
            algo,
            num_clusters,
            self.colorspace,
            self.rescaled_width,
        )
        return hist
