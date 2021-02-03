#!/usr/bin/env python3

import cv2
import logging
import numpy as np

from matplotlib import gridspec
from matplotlib import pyplot as plt
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


def get_hist_bar(hist, clust, img):
    img_height, img_width, _ = img.shape
    hist_bar_height = 60 #img_height
    hist_bar = np.zeros((hist_bar_height, img_width, 3), dtype = "uint8")
    startX = 0
    for (percent, color) in zip(hist, clust.cluster_centers_):
        endX = startX + (percent * img_width)
        cv2.rectangle(hist_bar, (int(startX), 0), (int(endX), hist_bar_height),
            color.astype("uint8").tolist(), -1)
        startX = endX
    return hist_bar


def plot_hist_bar(img, hist_bar):
    img_height, img_width, _ = img.shape
    canvas = plt.figure(
        figsize = (12.80, 7.20), 
        facecolor = "grey", 
        tight_layout = True
    )
    spec = gridspec.GridSpec(ncols=1, nrows=2, figure=canvas)
    screenshot = canvas.add_subplot(spec[0])
    plt.axis("off")
    palette = canvas.add_subplot(spec[1])
    plt.axis("off")
    screenshot.imshow(img, aspect="equal")
    palette.imshow(hist_bar, aspect="equal")
    plt.gca().set_box_aspect(img_height/img_width)
    pos0 = palette.get_position()
    pos1 = [pos0.x0, pos0.y0 - 0.18, pos0.width, pos0.height]
    palette.set_position(pos1)
    plt.show()

    return None
