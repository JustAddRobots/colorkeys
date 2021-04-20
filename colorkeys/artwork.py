#!/usr/bin/env python3

"""
This module facilitates creating an image matrix for data analysis.

    Typical Usage:

    my_artwork = Artwork("my_image_file.png")
"""

import errno
import logging
import os
import skimage.io as skiio
import skimage.color as skicolor
import skimage.transform as skitransform

logger = logging.getLogger(__name__)


class Artwork:
    """A class for loading image data and exposing underliying image properties.

    Attributes:
        imgsrc (str): Image source.
        colorspace (str): Color space of image.
        img (numpy.ndarray): Matrix of image data.
        img_height (int): Height of image.
        img_width (int): Width of image.
        num_channels (int): Number of channels in image.
        aspect_ratio (float): Aspect ratio of image.
        render (numpy.ndarray): Matrix of image rescaled for display.
        render_height (int): Height of display image.
        render_width (int): Width of display image.
    """

    def __init__(self, imgsrc, **kwargs):
        """Init Artwork.

        Args:
            imgsrc (str): Image source.

        **kwargs:
            colorspace (str): Color space of image.
        """
        self._imgsrc = self._get_imgsrc(imgsrc)
        self._colorspace = self._get_colorspace(kwargs)
        self._img = self._get_img()
        self._img_height, self._img_width, self._num_channels = self._img.shape
        self._aspect_ratio = self._img_width / self._img_height
        self._render_height = 400
        self._render_width = int(self.aspect_ratio * self._render_height)
        self._render = skitransform.rescale(
            self.img,
            (self.render_width / self.img_width),
            multichannel = True,
            anti_aliasing = True,
        )

    @property
    def imgsrc(self):
        "Image source"
        return self._imgsrc

    @property
    def colorspace(self):
        "Image color space"
        return self._colorspace

    @property
    def img(self):
        "Image matrix"
        return self._img

    @property
    def img_height(self):
        "Image height"
        return self._img_height

    @property
    def img_width(self):
        "Image width"
        return self._img_width

    @property
    def num_channels(self):
        "Image number of channels"
        return self._num_channels

    @property
    def aspect_ratio(self):
        "Image aspect ratio."
        return self._aspect_ratio

    @property
    def render(self):
        "Image matrix rescaled and for display"
        return self._render

    @property
    def render_height(self):
        "Image height"
        return self._render_height

    @property
    def render_width(self):
        "Image width"
        return self._render_width

    def show_debug(self):
        "Show class attribute debug information."
        return self._show_debug()

    def _get_imgsrc(self, imgsrc):
        """Get imgsrc.

        Checks the existence of requested img source, if local file.

        Args:
            imgsrc (str): Source name.

        Returns:
            imgsrc (str): Sourc name.

        Raises:
            FileNotFoundError: Requested file not found.
        """
        if not imgsrc.startswith(("http://", "https://")):
            if not os.path.exists(imgsrc):
                raise FileNotFoundError(
                    errno.ENOENT,
                    os.strerror(errno.ENOENT),
                    imgsrc
                )
        return imgsrc

    def _get_colorspace(self, kwargs):
        """Get image color space.

        An image is simply a matrix of data with no embedded color space information.
        So it is not possible to detect the color space. "RGB" is the assumed default.

        Args:
            None

        **kwargs:
            colorspace (str): Color space of requested image.

        Returns
            colorspace (str): Color space of requested image.

        Raises:
            TypeError: colorspace not a string.
            ValueError: colorspace not valid.
        """
        colorspace = kwargs.setdefault("colorspace", "RGB")
        if not isinstance(colorspace, str):
            raise TypeError("colorspace must be a string")
        if colorspace not in ["RGB", "HSV"]:
            raise ValueError(f"Invalid colorspace, {colorspace}")
        return colorspace

    def _get_img(self):
        """Get image matrix for the requested color space.

        Read image and convert to correct color space, if necessary.

        Args:
            None

        Returns:
            img (numpy.ndarray): Image matrix

        Raises:
            ValueError: colorspace not valid..
        """
        colorspace = self._colorspace
        img = skiio.imread(self._imgsrc)
        if colorspace == "RGB":
            pass
        elif colorspace == "HSV":
            img = skicolor.hsv2rgb(img)
        else:
            raise ValueError(f"Invalid colorspace, {colorspace}")

        return img
