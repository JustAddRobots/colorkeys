#!/usr/bin/env python3

"""
This module creates and displays color keys (palettes) from a requested image.

    Typical Usage:

    my_colorkey = ColorKey("my_image_file.png", ["kmeans"], 5)
    my_colorkey.show_palettes()
"""

import logging
import os.path

from matplotlib import gridspec
from matplotlib import pyplot as plt

from urllib.parse import urlparse

from colorkeys.artwork import Artwork
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
    def __init__(self, imgsrc, algos, num_clusters, **kwargs):
        super().__init__(imgsrc, **kwargs)
        """Init ColorKey.

        The number of color keys (palettes) generated for each image:
            len(algos) * len(colorspaces).

        Args:
            imgsrc (str): Image source.
            num_clusters (int): Number of clusters requested.
            algos (list): Algorithms requested.
        """
        self._hists = self._get_hists(algos, num_clusters)
        self._figure_size = (8.00, 4.50)  # (x100) px
        if self.imgsrc.startswith(("http://", "https://")):
            u = urlparse(self.imgsrc)
            self._figure_name = u.path.split("/")[-1]
        else:
            self._figure_name = os.path.basename(self.imgsrc)

    @property
    def hists(self):
        return self._hists

    def show_palettes(self):
        return self._show_palettes()

    def _get_hists(self, algos, num_clusters):
        """Get RGB and HSV histogram information for each algorithm requested.

        Args:
            num_clusters (int): Number of clusters requested.
            alogs (list): Algorithms requested.

        Returns:
            hists (dict): colorkeys.histogram.Hist objects keyed by algorithm
                and colorspace.
            Ex:
                hists["kmeans_RGB"] = colorkeys.histogram.Hist
        """
        hists = {}
        colorspaces = ("RGB", "HSV")
        for algo in algos:
            for colorspace in colorspaces:
                algo_cs = f"{algo}_{colorspace}"
                hists[algo_cs] = Hist(
                    self.img,
                    algo,
                    num_clusters,
                    colorspace,
                    self.render_width,
                )
        return hists

    def _show_palettes(self):
        """Show image and palette(s).

        Construct and show image + histogram bar on a grey canvas.
        Each bar is labelled by its algorithm + colorspace.

            +---------------------------------------+
            |                                       |
            |               image                   |
            |                                       |
            +---------------------------------------+

            +---------------------------------------+
            | histogram bar, algorithm, colorspace  |
            +---------------------------------------+
                                .
                                .
                                .
            +---------------------------------------+
            | histogram bar, algorithm, colorspace  |
            +---------------------------------------+

        Args:
            None

        Returns:
            None
        """
        # Create blank grey canvas.
        canvas = plt.figure(
            num = self._figure_name,
            figsize = self._figure_size,
            facecolor = "grey",
            tight_layout = {
                "rect": (0, 0, 1, 1),
            }
        )

        # Get histogram bar height from any Hist instance (all are same).
        any_hist = next(iter(self.hists.values()))
        hbar_height = any_hist.hist_bar_height

        # Create height ratios for histogram bars (1 bar / histogram)
        total_hbar_rows = len(self.hists)
        subplot_height_ratios = [
            (hbar_height / (self.render_height + hbar_height * total_hbar_rows))
        ] * total_hbar_rows

        # Insert image height ratio
        subplot_height_ratios.insert(
            0, (self.render_height / (self.render_height + hbar_height * total_hbar_rows))
        )

        # Create gridspec to include both image and histogram bar palettes.
        spec = gridspec.GridSpec(
            ncols = 1,
            nrows = 1 + total_hbar_rows,
            figure = canvas,
            height_ratios = subplot_height_ratios,
        )

        titlefont = {
            "fontsize": "medium",
            "color": "black"
        }

        # Add image to canvas.
        screenshot = canvas.add_subplot(spec[0])
        screenshot.grid(color="red", linestyle="-", linewidth=1)
        plt.axis("off")  # Switch "on" to troubleshoot layout.
        screenshot.imshow(self.render, aspect="equal")
        screenshot.set_title(
            fontdict = titlefont,
            label = (
                f"{self._figure_name}, "
                f"{self.img_width} x {self.img_height} px"
            ),
            loc = "center",
        )

        # Add histogram bar palettes to canvas.
        palettes = {}
        i = 1
        for algo_cs, h in self._hists.items():
            algo = algo_cs.split("_")[0]
            colorspace = algo_cs.split("_")[1]
            palettes[algo_cs] = canvas.add_subplot(spec[i])
            palettes[algo_cs].grid(color="red", linestyle="-", linewidth=1)
            plt.axis("off")
            palettes[algo_cs].imshow(h.hist_bar, aspect="equal")
            palettes[algo_cs].set_title(
                fontdict = titlefont,
                label = f"{algo}, {colorspace}, n_clusters = {h.num_clusters}",
                loc="center"
            )
            i += 1
        return None
