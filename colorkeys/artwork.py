#!/usr/bin/env python3

import cv2
import errno
import logging
import os

logger = logging.getLogger(__name__)


class Artwork:

    def __init__(self, filename, **kwargs):
        self._filename = self._get_filename(filename)
        self._colorspace = self._get_color_space(kwargs)
        self._img = self._get_img()
        self._height, self._width, self._num_channels = self._img.shape()

    @property
    def filename(self):
        "Image filename"
        return self._filename

    @property
    def color_space(self):
        "Image color space"
        return self._colorspace

    @property
    def img(self):
        "Image matrix"
        return self._img

    @property
    def height(self):
        "Image height"
        return self._height

    @property
    def width(self):
        "Image width"
        return self._width

    @property
    def num_channels(self):
        "Image number of channels"
        return self._num_channels

    def _get_filename(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                filename
            )
        return filename

    def _get_color_space(self, kwargs):
        colorspace = kwargs.setdefault("colorspace", "RGB")
        if not isinstance(colorspace, str):
            raise TypeError("colorspace must be a string")
        return colorspace

    def _get_img(self):
        colorspace = self._colorspace
        if colorspace == "RGB":
            cnv = cv2.COLOR_BGR2RGB
        elif colorspace == "HSV":
            cnv = cv2.COLOR_BGR2HSV
        img_BGR = cv2.imread(self._filename)
        img = cv2.cvtColor(img_BGR, cnv)
        return img
