#!/usr/bin/env python3

import cv2
import logging
import numpy as np

logger = logging.getLogger(__name__)

class Hist:

    def __init__(self, clust, img_width):
        self._hist_bar_height = 60
        self._clust = clust
        self._hist = self._get_hist()
        self._hist_bar = self._get_hist_bar(img_width)

    @property
    def hist(self):
        "Get histogram"
        return self._hist

    @property
    def hist_bar(self):
        "Get histogram bar"
        return self._hist_bar

    def _get_hist(self):
    	num_labels = np.arange(0, len(np.unique(self._clust.labels_)) + 1)
    	(hist, _) = np.histogram(self._clust.labels_, bins=num_labels)
    	hist = hist.astype("float")
    	hist /= hist.sum()
    	return hist

    def _get_hist_bar(img_width):
        num_channels = 3
        hist_bar = np.zeros(
            (self._hist_bar_height, img_width, num_channels), 
            dtype = "uint8",
        )
        start_x = 0
        for (percent, color) in zip(self._hist, self._clust.cluster_centers_):
            end_x = start_x + (percent * img_width)
            cv2.rectangle(
                hist_bar,
                (int(start_x), 0), 
                (int(end_x), self._hist_bar_height),
                color.astype("uint8").tolist(),
                -1,
            )
            start_x = end_x
        return hist_bar
