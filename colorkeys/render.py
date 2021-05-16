#!/usr/bin/env python3

import logging
import os.path

from matplotlib import gridspec
from matplotlib import pyplot as plt
from urllib.parse import urlparse

from colorkeys.constants import _const as CONSTANTS

logger = logging.getLogger(__name__)


class Layout():
    """A class to layout and render a single image with associated palette/histogram
    information for each respective algorithm + colorspace combination.

    This class expects a list of palettes (colorkeys.ColorKey). Each palette contains
    the same image source, but different histogram information.

    The size of the canvas is determined by CONSTANTS().FIGURE_SIZE. The
    image is rescaled based on CONSTANTS().RESCALED_HEIGHT.

    The layout and render process involves the following steps:
        1. Create a blank grey canvas onto which all information will be rendered.
        2. Create a grid on the canvas that will contain the images and histogram(s).
        3. Add the image to the layout grid.
        4. Add each histogram info to the layout grid.
    """
    def __init__(self, palettes):
        self._palettes = palettes
        self._any_palette = next(iter(self._palettes))
        self._figure_size = CONSTANTS().FIGURE_SIZE
        self._figure_name = self._get_figure_name()
        self._canvas = self._create_canvas()
        self._grid = self._create_layout()
        self._titlefont = {
            "fontsize": "medium",
            "color": "black"
        }

    def draw_palettes(self):
        """Layout and render image and palette info"""
        return self._draw_palettes()

    def _draw_palettes(self):
        self._add_image_to_canvas()
        self._add_hist_bars_to_canvas()
        return None

    def _get_figure_name(self):
        """Get the figure name.

        Args:
            None

        Returns:
            figure_name
        """
        if self._any_palette.imgsrc.startswith(("http://", "https://")):
            u = urlparse(self._any_palette.imgsrc)
            figure_name = u.path.split("/")[-1]
        else:
            figure_name = os.path.basename(self._any_palette.imgsrc)
        return figure_name

    def _create_canvas(self):
        """Create blank grey canvas, using figure info.

        Args:
            None

        Returns:
            canvas (pyplot.figure): Canvas on which to layout and plot images.
        """
        canvas = plt.figure(
            num = self._figure_name,
            figsize = self._figure_size,
            facecolor = "grey",
            tight_layout = {
                "rect": (0, 0, 1, 1),
            }
        )
        return canvas

    def _create_layout(self):
        """Create a layout grid from instance's palette list. The first grid row
        is the instance image and subsequent grid rows are histogram bars.

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
        """
        art = self._canvas.add_subplot(self._grid[0])
        art.grid(color="red", linestyle="-", linewidth=1)
        plt.axis("off")  # Switch "on" to troubleshoot layout.
        art.imshow(self._any_palette.img_rescaled, aspect="equal")
        art.set_title(
            fontdict = self._titlefont,
            label = (
                f"{self._figure_name}, "
                f"{self._any_palette.img_width} x {self._any_palette.img_height} px"
            ),
            loc = "center",
        )
        return None

    def _add_hist_bars_to_canvas(self):
        """Add histogram bars from palette list to canvas."""
        bars = {}
        i = 1  # grid row
        for p in self._palettes:
            algo_cs = f"{p.hist.algo}_{p.hist.colorspace}"
            bars[algo_cs] = self._canvas.add_subplot(self._grid[i])
            bars[algo_cs].grid(color="red", linestyle="-", linewidth=1)
            plt.axis("off")
            bars[algo_cs].imshow(p.hist.hist_bar, aspect="equal")
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
