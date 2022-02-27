#!/usr/bin/env python3

"""
This module facilitates numerical analysis of color information across
clusters and samples.

Cluster centroid matrices are extracted from colorkeys object and translated
into a format for analysis.

sample #0                               sample #1
cluster 0: [ R00, G00, G00, percent00]  [ R01, G01, B01, percent01]
cluster 1: [ R10, G10, B10, percent10]  [ R11, G11, B11, percent11]

...translated to...

cluster 0: [ R00, G00, B00, percent00]  |       |
           [ R01, G01, B01, percent01]  |       |
                                        v       v
                                        mean    std
cluster 1: [ R10, G10, B10, percent10]
           [ R11, G11, B11, percent11]

The mean and std for each cluster can then be computed for each element of
the row vector ([R, G, B, percent]) along the Y axis.
"""

import numpy as np


def get_cluster_means(clusters):
    """Get the arithmetic mean of each cluster.

    Args:
        clusters (dict): Color & percent values, key is cluster number
            value is 2D array of n samples with row vector ([R, G, B, percent]).

    Returns:
        means (dict): key is cluster number (0, num_clusters)
            value is mean of each cluster as vector ([R, G, B, percent]).
    """
    means = {}
    for i, cluster in clusters.items():
        means[i] = np.mean(cluster, axis=0)
    return means


def get_cluster_stds(clusters):
    """Get the standard deviation of each cluster.

    Args:
        clusters (dict): Color & percent values, key is cluster number
            value is 2D array of n samples with row vector ([R, G, B, percent]).

    Returns:
        stds (dict): key is cluster number (0, num_clusters)
            value is std of each cluster as vector ([R, G, B, percent]).
    """
    stds = {}
    for i, cluster in clusters.items():
        stds[i] = np.std(cluster, axis=0)
    return stds


def get_centroids(colorkeys):
    """Get centroid matrices of colorkey objects.

    Args:
        colorkeys (list): colorkey objects.

    Returns:
        centroids (dict): Cluster centroids, key is cluster number (0, num_clusters)
            value is 2D array with row vector ([R, G, B, percent]).
    """
    centroids = {}
    for i, colorkey in enumerate(colorkeys):
        centroids[i] = create_matrix(colorkey)
    return centroids


def create_matrix(colorkey):
    """Create centroid matrix from colorkey object.

    Extract the centroid information from colorkey object.

    Args:
        colorkey (colorkeys.ColorKey): colorkey information.

    Returns:
        matrix (numpy.ndarray): row vector ([R, G, B, percent]).
    """
    centroids = colorkey["histogram"]["hist_centroids"]
    m = []
    for i in centroids:
        row = i["color"] + [i["percent"]]
        m.append(row)
    matrix = np.array(m)
    return matrix


def get_centroids_by_cluster(centroids):
    """Get matrix of centroids stacked by cluster row.

    Stack i^th row of each sample into 2D array. This allows easy calculation
    of mean and std of the i^th cluster for all samples

    Args:
        centroids (dict): Centroid info, key is cluster number,
            value is row vector ([R, G, B, percent).

    Returns:
        clusters (dict): 2D array of row vectors, key is cluster number,
            value is 2D array of vector ([R, G, B]), one row per sample.
    """
    if is_same_shape(centroids):
        clusters = {}
        for centroid in centroids.values():
            for j in range(0, centroid.shape[0]):
                row = centroid[j:j + 1]
                if j not in clusters.keys():
                    clusters[j] = row
                else:
                    clusters[j] = np.vstack((clusters[j], row))
    return clusters


def is_same_shape(centroids):
    """Check if centroid matrices have the same shape.

    Identical matrix shape is required for some matrix operations.

    Args:
        centroids (dict): Centroid info, key is cluster number,
            value is row vector ([R, G, B, percent).

    Returns:
        same_shape (bool): True if all centroids in dict are same shape.
    """
    same_shape = True
    shape = ()
    for m in centroids.values():
        if not shape:
            shape = m.shape
        elif shape != m.shape:
            same_shape = False
            break
    return same_shape
