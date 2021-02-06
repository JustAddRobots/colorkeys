#!/usr/bin/env python3

import cv2
import logging

from matplotlib import gridspec
from matplotlib import pyplot as plt

from colorkeys.artwork import Artwork
from colorkeys.centroids import Clust
from colorkeys.histogram import Hist

logger = logging.getLogger(__name__)


class ColorKey(Artwork):

    def __init__(self, filename, num_clusters, algos, **kwargs):
        super().__init__(filename, **kwargs)

        self._hists = self._get_hists(num_clusters, algos)
        self._figure_size = (8.00, 4.50)  # (x100) px

    @property
    def hists(self):
        return self._hists

    def show_img(self):
        return self._show_img()

    def show_palettes(self):
        return self._show_palettes()

    def _get_hists(self, num_clusters, algos):
        hists = {}
        for algo in algos:
            c = Clust(self.img, num_clusters, algo)
            h = Hist(c.clust, num_clusters, self.img_width)
            hists[algo] = h
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
        canvas = plt.figure(
            figsize = self._figure_size,
            facecolor = "grey",
            tight_layout = True
        )
        hbar_height = next(iter(self.hists.values())).hist_bar_height
        total_rows = len(self.hists) + 1
        spec = gridspec.GridSpec(
            ncols = 1,
            nrows = total_rows,
            figure = canvas,
            height_ratios = [
                (self.img_height / (self.img_height + hbar_height)),
                (hbar_height / (self.img_height + hbar_height)),
            ]
        )
        screenshot = canvas.add_subplot(spec[0])
        screenshot.grid(color="red", linestyle="-", linewidth=1)
        plt.axis("off")
        screenshot.imshow(self.img, aspect="equal")
        screenshot.set_title(
            label = "{0}, {1} x {2} px".format(
                self.filename,
                self.img_width,
                self.img_height,
            ),
            loc = "left",
        )
        palettes = {}
        for algo, h in self._hists.items():
            i = 1
            palettes[algo] = canvas.add_subplot(spec[i])
            palettes[algo].grid(color="red", linestyle="-", linewidth=1)
            plt.axis("off")
            palettes[algo].imshow(h.hist_bar, aspect="equal")
            palettes[algo].set_title(
                label = "{0}, n_clusters = {1}".format(algo, h.num_clusters),
                loc="left"
            )
            i += 1
        plt.show()
        return None