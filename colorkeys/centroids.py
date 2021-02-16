#!/usr/bin/env python3

"""
This module facilitates cluster creation.

    Typical Usage:

    my_cluster = Clust(img_matrix, "kmeans", 5)
"""

import logging

from sklearn import cluster
from sklearn import neighbors

logger = logging.getLogger(__name__)


class Clust:
    """A class for generating centroids/clusters based on the requested algorithm.

    https://scikit-learn.org/stable/modules/classes.html#module-sklearn.cluster
    https://en.wikipedia.org/wiki/K-means_clustering
    https://en.wikipedia.org/wiki/Hierarchical_clustering

    Attributes:
        clust (sklearn.cluster): Cluster generated.
        centroids (numpy.ndarray): Centroids generated.
        num_clusters (int): Number of clusters/centroids requested.
    """
    def __init__(self, img, algo, num_clusters):
        """Init Clust.

        Args:
            img (numpy.ndarray): Matrix of image data.
            algo (str): Algorithm requested for clusters/centroids generated.
            num_clusters (int): Number of clusters/centroids requested.
        """
        # Convert 2D array to 1D for cluster generation.
        img_reshape = img.reshape(img.shape[0] * img.shape[1], img.shape[2])
        self._clust = self._get_clust(img_reshape, algo, num_clusters)
        self._centroids = self._get_centroids(img_reshape, algo)
        self._num_clusters = num_clusters

    @property
    def clust(self):
        return self._clust

    @property
    def centroids(self):
        return self._centroids

    @property
    def num_clusters(self):
        return self._num_clusters

    def _get_clust(self, img, algo, n):
        """Get cluster.

        Args:
            img (numpy.ndarray): Matrix of image data.
            algo (str): Algorithm requested for clusters generated.
            n (int): Number of clusters/centroids requested.

        Returns:
            clust (sklearn.cluster): Generated cluster.
        """
        if algo == "kmeans":  # K-Means Clustering
            clust = cluster.KMeans(n_clusters=n)
        elif algo == "hac":  # Heirarchical Agglomerative Clustering
            clust = cluster.AgglomerativeClustering(n_clusters=n)
        return clust

    def _get_centroids(self, img, algo):
        """Get centroids from cluster.

        Args:
            img (numpy.ndarray): Matrix of image data.
            algo (str): Algorithm requested for centroids generated.

        Returns:
            centroids (numpy.ndarray): Array of centroids.
        """
        if algo == "kmeans":
            self._clust.fit(img)
            centroids = self._clust.cluster_centers_
        elif algo == "hac":
            predict = self._clust.fit_predict(img)
            clf = neighbors.NearestCentroid()
            clf.fit(img, predict)
            centroids = clf.centroids_
        return centroids
