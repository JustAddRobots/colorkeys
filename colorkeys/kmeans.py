#!/usr/bin/env python3

import cv2
import logging
import numpy as np

from matplotlib import pyplot
from sklearn import cluster

logger = logging.getLogger(__name__)


def get_img_rgb(filename):
    img = cv2.imread(filename)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb


def show_img(filename):
    pyplot.imshow(img_rgb)
    pyplot.show()
    return None


def get_clusters(k, img):
    clust = cluster.KMeans(n_clusters=k)
    return clust


def get_cluster_histogram(clust):
    num_labels = np.arange(0, len(np.unique(clust.labels_)) + 1)
    (hist, _) = np.histogram(clust.labels_, bins=num_labels)
    hist = hist.astype("float")
    hist /= hist.sum()
    return hist


def get_hist_bar(hist, clust):
    hist_bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0
    for (percent, color) in zip(hist, clust.cluster_centers_):
        endX = startX + (percent * 300)
        cv2.rectangle(hist_bar, (int(startX), 0), (int(endX), 50),
            color.astype("uint8").tolist(), -1)
        startX = endX
    return hist_bar


def plot_hist_bar(img, hist_bar)
    pyplot.figure(figsize=(10,10))
    pyplot.subplot(121)
    pyplot.imshow(img)
    pyplot.axis("off")
    pyplot.subplot(122)
    pyplot.imshow(hist_bar)
    pyplot.axis("off")
    pyplot.show()
    return None
