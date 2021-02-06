#!/usr/bin/env python3

from sklearn import cluster


def test_clust(myclust):
    assert isinstance(myclust.clust, cluster._kmeans.KMeans)


def test_num_clusters(myclust):
    assert myclust.num_clusters == 5
