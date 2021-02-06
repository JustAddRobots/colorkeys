#!/usr/bin/env python3

import cv2
import errno
import logging
import os

logger = logging.getLogger(__name__)


class Artwork:

    def __init__(self, filename, **kwargs):
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

    @property
    def show_debug(self):
        return self._show_debug()

    def _get_filename(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                filename
            )
        return filename

    def _get_colorspace(self, kwargs):
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

    def _show_debug(self):
        attrs = vars(self)
        for k, v in attrs.items():
            if k.startswith("_"):
                logger.debug("{0}: {1}".format(k, v))
        return None
