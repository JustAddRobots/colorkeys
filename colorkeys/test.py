#!/usr/bin/env python3

import cv2

from matplotlib import pyplot
from sklearn import cluster


def get_img_rgb(filename):
    img = cv2.imread(filename)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb


def show_img(filename):
    pyplot.imshow(img_rgb)
    pyplot.show()
    return None


def get_clusters(img, k):
    clust = cluster.KMeans(n_clusters=k)
    return clust


if __name__ == "__main__":
    imgfile = "/Users/rcon/Sandbox/git/colorkeys-samples/square/tumblr_om39hc6cTV1qbk6ogo1_1280.png"
    img = get_img_rgb(filename=imgfile)
    k = 5
    clust = get_clusters(image=img, k)
