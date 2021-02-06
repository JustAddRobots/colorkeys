#!/usr/bin/env python3

import logging

from sklearn import cluster

logger = logging.getLogger(__name__)


class Clust:

    def __init__(self, img, num_clusters, algo):
        img_reshape = img.reshape(img.shape[0] * img.shape[1], img.shape[2])
        self._clust = self._get_clust(img_reshape, num_clusters, algo)
        self._num_clusters = num_clusters

    @property
    def clust(self):
        return self._clust

    @property
    def num_clusters(self):
        return self._num_clusters

    def _get_clust(self, img, n, algo):
        if algo == "kmeans":  # K-Means Clustering
            clust = cluster.KMeans(n_clusters=n)
        elif algo == "hac":  # Heirarchical Agglomerative Clustering
            clust = cluster.AgglomerativeClustering(n_clusters=n)
        clust.fit(img)
        return clust
