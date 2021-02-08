#!/usr/bin/env python3

"""
This module facilitates creating an image matrix for data analysis.

    Typical Usage:

    my_artwork = Artwork("my_image_file.png")
"""

import cv2
import errno
import logging
import os

logger = logging.getLogger(__name__)


class Artwork:
    """A class for loading image data and exposing underliying image properties.

    Attributes:
        filename (str): Image filename.
        colorspace (str): Color space of image.
        img (numpy.ndarray): Matrix of image data.
        img_height (int): Height of image.
        img_width (int): Width of image.
        num_channels (int): Number of channels in image.
    """

    def __init__(self, filename, **kwargs):
        """Init Artwork.

        Args:
            filename(str): Image filename.

        **kwargs:
            colorspace (str): Color space of image.
        """
        self._filename = self._get_filename(filename)
        self._colorspace = self._get_colorspace(kwargs)
        self._img = self._get_img()
        self._img_height, self._img_width, self._num_channels = self._img.shape

    @property
    def filename(self):
        "Image filename"
        return self._filename

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

    def show_debug(self):
        "Show class attribute debug information."
        return self._show_debug()

    def _get_filename(self, filename):
        """Get filename.

        Checks the existence of requested file.

        Args:
            filename (str): File name.

        Returns:
            filename (str): File name.

        Raises:
            FileNotFoundError: Requested file not found.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                filename
            )
        return filename

    def _get_colorspace(self, kwargs):
        """Get image color space.

        An image is simply a matrix of data with no embedded color space information.
        So it is not possible to detect the color space.

        Args:
            None

        **kwargs:
            colorspace (str): Color space of requested image.

        Returns
            colorspace (str): Color space of requested image.

        Raises:
            TypeError: colorspace not a string.
        """
        colorspace = kwargs.setdefault("colorspace", "RGB")
        if not isinstance(colorspace, str):
            raise TypeError("colorspace must be a string")
        return colorspace

    def _get_img(self):
        """Get image matrix for the requested color space.

        cv2 automatically reads the image as BGR, so it must be converted to the
        correct color space. For now, assume all images will be RBG. HSV will be
        used for algorithm testing at a later date.

        Args:
            None

        Returns:
            img (numpy.ndarray): Image matrix.
        """
        colorspace = self._colorspace
        if colorspace == "RGB":
            cnv = cv2.COLOR_BGR2RGB
        elif colorspace == "HSV":
            cnv = cv2.COLOR_BGR2HSV
        img_BGR = cv2.imread(self._filename)
        img = cv2.cvtColor(img_BGR, cnv)
        return img

    def _show_debug(self):
        attrs = vars(self)
        for k, v in attrs.items():
            if k.startswith("_"):
                logger.debug("{0}: {1}".format(k, v))
        return None
