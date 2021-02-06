#!/usr/bin/env python3

"""
This module facilitates cluster creation.

    Typical Usage:

    my_cluster = Clust(img_matrix, 5, "kmeans")
"""

import logging

from sklearn import cluster

logger = logging.getLogger(__name__)


class Clust:
    """A class for generating centroids/clusters based on the requested algorithm.

    https://scikit-learn.org/stable/modules/classes.html#module-sklearn.cluster
    https://en.wikipedia.org/wiki/K-means_clustering
    https://en.wikipedia.org/wiki/Hierarchical_clustering

    Attributes:
        clust (sklearn.cluster): Cluster generated.
        num_clusters (int): Number of clusters/centroids requested.
    """
    def __init__(self, img, num_clusters, algo):
        """Init Clust.

        Args:
            img (numpy.ndarray): Matrix of image data.
            num_clusters (int): Number of clusters/centroids requested.
            algo (str): Algorithm requested for clusters/centroids generated.
        """
        # Convert 2D array to 1D for cluster generation.
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
        """Get cluster.

        Args:
            img (numpy.ndarray): Matrix of image data.
            n (int): Number of clusters/centroids requested.
            algo (str): Algorithm requested for clusters/centroids generated.

        Returns:
            clust (sklearn.cluster): Generated clusters/centroids.
        """
        if algo == "kmeans":  # K-Means Clustering
            clust = cluster.KMeans(n_clusters=n)
        elif algo == "hac":  # Heirarchical Agglomerative Clustering
            clust = cluster.AgglomerativeClustering(n_clusters=n)
        clust.fit(img)
        return clust
