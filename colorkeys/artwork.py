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

from colorkeys.constants import _const as CONSTANTS

logger = logging.getLogger(__name__)


class Artwork:
    """A class for loading image data and exposing underliying image properties.

    Attributes:
        imgsrc (str): Image source.
        img_colorspace (str): Color space of image.
        img (numpy.ndarray): Matrix of image data.
        img_height (int): Height of image.
        img_width (int): Width of image.
        num_channels (int): Number of channels in image.
        aspect_ratio (float): Aspect ratio of image.
        img_rescaled (numpy.ndarray): Matrix of image rescaled for display.
        rescaled_height (int): Height of display image.
        rescaled_width (int): Width of display image.
    """

    def __init__(self, imgsrc, **kwargs):
        """Init Artwork.

        Args:
            imgsrc (str): Image source.

        **kwargs:
            colorspace (str): Color space of image.
        """
        self._imgsrc = self._get_imgsrc(imgsrc)
        self._img_colorspace = self._get_colorspace()
        self._img = self._get_img()
        self._img_height, self._img_width, self._num_channels = self._img.shape
        self._aspect_ratio = self._img_width / self._img_height
        self._rescaled_height = CONSTANTS().RESCALED_HEIGHT
        self._rescaled_width = int(self.aspect_ratio * self._rescaled_height)
        self._img_rescaled = skitransform.rescale(
            self.img,
            (self.rescaled_width / self.img_width),
            multichannel = True,
            anti_aliasing = True,
        )

    @property
    def imgsrc(self):
        "Image source location"
        return self._imgsrc

    @property
    def img_colorspace(self):
        "Image color space"
        return self._img_colorspace

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
    def img_rescaled(self):
        "Image matrix rescaled for display"
        return self._img_rescaled

    @property
    def rescaled_height(self):
        "Image height"
        return self._rescaled_height

    @property
    def rescaled_width(self):
        "Image width"
        return self._rescaled_width

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

    def _get_colorspace(self):
        """Get image color space.

        An image is simply a matrix of data with no embedded color space information.
        So it is not possible to detect the color space. Make "RGB" the default.

        Args:
            None

        Returns
            colorspace (str): Color space of requested image.

        Raises:
            TypeError: colorspace not a string.
            ValueError: colorspace not valid.
        """
        colorspace = CONSTANTS().DEFAULT_COLORSPACE
        if not isinstance(colorspace, str):
            raise TypeError("colorspace must be a string")
        if colorspace not in ["RGB", "HSV"]:
            raise ValueError(f"Invalid colorspace, {colorspace}")
        return colorspace

    def _get_img(self):
        """Get image matrix for the requested color space.

        Read image and convert to correct color space, if necessary. Disregard alpha
        channel.

        Args:
            None

        Returns:
            img (numpy.ndarray): Image matrix

        Raises:
            ValueError: colorspace not valid..
        """
        img = skiio.imread(self._imgsrc)
        if img.shape[2] == 4:
            img = img[:, :, :3]  # Disregard alpha channel

        if self._img_colorspace == "RGB":
            pass
        elif self._img_colorspace == "HSV":
            img = skicolor.hsv2rgb(img)
        else:
            raise ValueError(f"Invalid colorspace, {self._img_colorspace}")
        return img
