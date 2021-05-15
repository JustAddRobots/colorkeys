#!/usr/bin/env python3

import logging
import os.path

from matplotlib import gridspec
from matplotlib import pyplot as plt
from urllib.parse import urlparse

from colorkeys.constants import _const as CONSTANTS

logger = logging.getLogger(__name__)


class Layout():

    def __init__(self, palettes):
        self._palettes = palettes
        self._any_palette = next(iter(self._palettes))
        self._canvas = self._create_canvas()
        self._grid = self._create_layout()
        self._titlefont = {
            "fontsize": "medium",
            "color": "black"
        }

    def draw_palettes(self):
        return self._draw_palettes()

    def _draw_palettes(self):
        self._add_image_to_canvas()
        self._add_hist_bars_to_canvas()
        return None

    def _create_canvas(self):
        """Create blank grey canvas, using instance palette info.

        Args:
            None

        Returns:
            canvas (pyplot.figure): Canvas on which layout and plot images.
        """
        figure_size = CONSTANTS().FIGURE_SIZE
        if self._any_palette.imgsrc.startswith(("http://", "https://")):
            u = urlparse(self.imgsrc)
            figure_name = u.path.split("/")[-1]
        else:
            figure_name = os.path.basename(self.imgsrc)

        canvas = plt.figure(
            num = figure_name,
            figsize = figure_size,
            facecolor = "grey",
            tight_layout = {
                "rect": (0, 0, 1, 1),
            }
        )
        return canvas

    def _create_layout(self):
        """Create a layout grid from instance's palette list. The first grid row
        is instance image and histogram bars are subsequent grid rows.

        Args:
            None

        Returns:
            grid (gridspec.GridSpec): Gridspec layout of image and histogram bars.

        The gridspec layout will look like the following:

            +---------------------------------------+
            |                                       |
            |            image (rescaled)           |   grid[0]
            |                                       |
            +---------------------------------------+

            +---------------------------------------+
            | histogram bar, algorithm, colorspace  |   grid[1], from palette #1
            +---------------------------------------+
                                .
                                .
                                .
            +---------------------------------------+
            | histogram bar, algorithm, colorspace  |   grid[N], from palette #N
            +---------------------------------------+
        """
        # Get histogram bar height from any palette
        hbar_height = self._any_palette.hist.hist_bar_height

        # Create height ratios for histogram bar rows using scaled image height
        total_hbar_rows = len(self._palettes)
        subplot_height_ratios = [(
            hbar_height
            / (self._any_palette.rescaled_height + hbar_height * total_hbar_rows)
        )] * total_hbar_rows

        # Insert image rescaled height ratio for grid[0]
        subplot_height_ratios.insert(
            0,
            (
                self._any_palette.rescaled_height
                / (self._any_palette.rescaled_height + hbar_height * total_hbar_rows)
            )
        )

        grid = gridspec.GridSpec(
            ncols = 1,
            nrows = 1 + total_hbar_rows,
            figure = self._canvas,
            height_ratios = subplot_height_ratios,
        )
        return grid

    def _add_image_to_canvas(self):
        """Add image to the canvas. Use any palette instance since they all are
        based on the same image data.

        Args:
            None

        Returns:
            None
        """
        art = self._canvas.add_subplot(self._grid[0])
        art.grid(color="red", linestyle="-", linewidth=1)
        plt.axis("off")  # Switch "on" to troubleshoot layout.
        art.imshow(self._any_palette.img_rescaled, aspect="equal")
        art.set_title(
            fontdict = self._titlefont,
            label = (
                f"{self._any_palette.figure_name}, "
                f"{self._any_palette.img_width} x {self._any_palette.img_height} px"
            ),
            loc = "center",
        )
        return None

    def _add_hist_bars_to_canvas(self):
        """Add histogram bars from palette list to canvas.

        Args:
            None

        Returns:
            None
        """
        bars = {}
        i = 1  # grid row
        for p in self._palettes:
            algo_cs = f"{p.hist.algo}_{p.hist.colorspace}"
            bars[algo_cs] = self._canvas.add_subplot(self._grid[i])
            bars[algo_cs].grid(color="red", linestyle="-", linewidth=1)
            plt.axis("off")
            bars.imshow(p.hist.hist_bar, aspect="equal")
            bars[algo_cs].set_title(
                fontdict = self._titlefont,
                label = (
                    f"{p.hist.algo}, {p.hist.colorspace}, "
                    f"n_clusters = {p.hist.num_clusters}"
                ),
                loc="center"
            )
            i += 1
        return None
