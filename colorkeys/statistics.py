#!/usr/bin/env python3

import numpy as np


def get_cluster_means(clusters):
    means = {}
    for i, cluster in clusters.items():
        means[i] = np.mean(cluster, axis=0)
    return means


def get_cluster_stds(clusters):
    stds = {}
    for i, cluster in clusters.items():
        stds[i] = np.std(cluster, axis=0)
    return stds


def get_centroids(colorkeys):
    """Get centroid matrices.
    """
    centroids = {}
    for i, colorkey in enumerate(colorkeys):
        centroids[i] = create_matrix(colorkey)
    return centroids


def create_matrix(colorkey):
    """Create centroid matrix from colorkey object.
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
    """Check if centroids have the same shape.

    Identical matrix shape is required for some matrix operations.
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
