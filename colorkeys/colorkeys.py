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

    @property
    def hists(self):
        return self._hists

    @property
    def show_img(self):
        return self._show_img()

    @property
    def show_palettes(self):
        return self._show_palettes()

    def _get_hists(self, num_clusters, algos):
        hists = {}
        for algo in algos:
            c = Clust(self.img, num_clusters, algo)
            h = Hist(c.clust, self.width)
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
            figsize = (12.80, 7.20),
            facecolor = "grey",
            tight_layout = True
        )
        total_rows = len(self._hists) + 1
        spec = gridspec.GridSpec(ncols=1, nrows=total_rows, figure=canvas)
        screenshot = canvas.add_subplot(spec[0])
        plt.axis("off")
        screenshot.imshow(self.img, aspect="equal")
        for i in range(1, len(self._hists) + 1):
            canvas.add_subplot(spec[i])
            plt.axis("off")
            plt.gca().set_box_aspect(self.height / self.width)
        plt.show()

#         palette = canvas.add_subplot(spec[1])
#         plt.axis("off")
#         screenshot.imshow(img, aspect="equal")
#         palette.imshow(hist_bar, aspect="equal")
#         plt.gca().set_box_aspect(img_height/img_width)
#         pos0 = palette.get_position()
#         pos1 = [pos0.x0, pos0.y0 - 0.18, pos0.width, pos0.height]
#         palette.set_position(pos1)
#         plt.show()
        return None
