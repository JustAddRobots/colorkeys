#!/usr/bin/env python3

"""
This module creates and displays color keys (palettes) from a requested image.

    Typical Usage:

    my_colorkey = ColorKey("my_image_file.png", 5, ["kmeans"])
    my_colorkey.show_palettes()
"""

import cv2
import logging

from matplotlib import gridspec
from matplotlib import pyplot as plt

from colorkeys.artwork import Artwork
from colorkeys.histogram import Hist

logger = logging.getLogger(__name__)
mpl_logger = logging.getLogger("matplotlib")
mpl_logger.setLevel(logging.WARNING)


class ColorKey(Artwork):
    """A class for loading, generating, and displaying image color keys.

    Attributes:
        hists (dict): colorkeys.histogram.Hist(s) keyed by requested algorithm.
        show_palettes (None): Display image(s) and palette(s).
    """
    def __init__(self, filename, algos, num_clusters, **kwargs):
        super().__init__(filename, **kwargs)
        """Init ColorKey.

        The number of color keys (palettes) generated for each image:
            len(algos) * len(colorspace).

        Args:
            filename (str): Image filename.
            num_clusters (int): Number of clusters requested.
            algos (list): Algorithms requested.
        """
        self._hists = self._get_hists(algos, num_clusters)
        self._figure_size = (8.00, 4.50)  # (x100) px

    @property
    def hists(self):
        return self._hists

    def show_img(self):
        return self._show_img()

    def show_palettes(self):
        return self._show_palettes()

    def _get_hists(self, algos, num_clusters):
        """Get RGB and HSV histogram information for each algorithm requested.

        Args:
            num_clusters (int): Number of clusters requested.
            alogs (list): Algorithms requested.

        Returns:
            hists (dict): colorkeys.histogram.Hist(s) keyed by algorithm.
        """
        hists = {}
        hist_colorspaces = ["RGB", "HSV"]
        for algo in algos:
            h_dict = {}
            for hist_colorspace in hist_colorspaces:
                h_dict[hist_colorspace] = Hist(
                    self.img,
                    algo,
                    num_clusters,
                    hist_colorspace,
                    self.img_width
                )
            hists[algo] = h_dict
        return hists

    def _show_img(self):
        if self.colorspace == "HSV":
            img_RGB = cv2.cvtColor(self.img, cv2.COLOR_HSV2RGB)
        elif self.colorspace == "RGB":
            img_RGB = self.img
        plt.imshow(img_RGB)
        plt.show()
        return None

    def _show_palettes(self):
        """Show image and palette(s).

        Args:
            None

        Returns:
            None
        """
        # create blank grey canvas
        canvas = plt.figure(
            figsize = self._figure_size,
            facecolor = "grey",
            tight_layout = True
        )

        # get histogram bar height from any Hist instance (fixed for all)
        any_h_clrspace = next(iter(self.hists.values()))
        hbar_height = next(iter(any_h_clrspace.values())).hist_bar_height

        # set height ratios for img and histogram bars
        total_hbar_rows = len(self.hists) + len(self.hists.values())
        subplot_height_ratios = [
            (hbar_height / (self.img_height + hbar_height * total_hbar_rows))
        ] * total_hbar_rows
        subplot_height_ratios.insert(
            0, (self.img_height / (self.img_height + hbar_height * total_hbar_rows))
        )

        # create gridspec to include both img and histogram bar palettes
        spec = gridspec.GridSpec(
            ncols = 1,
            nrows = 1 + total_hbar_rows,
            figure = canvas,
            height_ratios = subplot_height_ratios
        )

        # add image to canvas
        screenshot = canvas.add_subplot(spec[0])
        screenshot.grid(color="red", linestyle="-", linewidth=1)
        plt.axis("off")  # used for troubleshooting grid
        screenshot.imshow(self.img, aspect="equal")
        screenshot.set_title(
            fontdict = {
                "fontsize": "medium",
                "color": "black"
            },
            label = "{0}, {1} x {2} px".format(
                self.filename,
                self.img_width,
                self.img_height,
            ),
            loc = "center",
        )

        # add histogram bar palettes to canvas
        palettes = {}
        i = 1
        for algo, h_colorspaces in self._hists.items():
            for colorspace, h in h_colorspaces.items():
                algo_cs = "{0}-{1}".format(algo, colorspace)
                palettes[algo_cs] = canvas.add_subplot(spec[i])
                palettes[algo_cs].grid(color="red", linestyle="-", linewidth=1)
                plt.axis("off")
                palettes[algo_cs].imshow(h.hist_bar, aspect="equal")
                palettes[algo_cs].set_title(
                    label = "{0}, {1}, n_clusters = {2}".format(
                        algo,
                        colorspace,
                        h.num_clusters
                    ),
                    loc="center"
                )
                i += 1
        plt.ioff()
        _ = plt.show(block=False)
        return None
