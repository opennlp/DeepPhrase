# -*- coding: utf-8 -*-
"""
Module to act as a wrapper for different clustering algorithms
"""

from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AffinityPropagation
from clusterwrapper.clustermetrics import get_calinski_harabaz_coefficient, get_silhouette_coefficient

"""
Wrapper around the KMeans class of sklearn, allows easy interface with the functions
It has already some default parameters set like number of clusters and maximum iterations
"""


class KMeansClustering:
    def __init__(self, n_clusters=5, max_iter=300, random_state=42):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.kmeans_object = KMeans(n_clusters=self.n_clusters, max_iter=self.max_iter, random_state=self.random_state)

    def fit_data(self, X):
        return self.kmeans_object.fit(X)

    def get_cluster_labels(self):
        return self.kmeans_object.labels_

    def get_cluster_centers(self):
        return self.kmeans_object.cluster_centers_

    def get_silhouette_score(self, X):
        return get_silhouette_coefficient(X, self.kmeans_object.labels_)

    def get_calinski_harabiz_score(self, X):
        return get_calinski_harabaz_coefficient(X, self.kmeans_object.labels_)


"""
Wrapper around the dbscan class of sklearn providing easy to use APIs
It has some parameters already initialized like epsilon and min_samples
"""


class DBSCANClustering:
    def __init__(self, eps=0.5, min_samples=5, metric='euclidean', leaf_size=30):
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.leaf_size = leaf_size
        self.dbscan_object = DBSCAN(eps=self.eps, min_samples=self.min_samples, leaf_size=self.leaf_size,metric='euclidean')

    def fit_data(self, X):
        self.dbscan_object.fit(X)

    def get_cluster_labels(self):
        return self.dbscan_object.labels_

    def get_core_components(self):
        return self.dbscan_object.components_

    def get_core_sample_indices(self):
        return self.dbscan_object.core_sample_indices_


"""
A Wrapper around the Affinity Propagation class of sklearn providing easy to use APIs
It only sets the affinity metric to euclidean as a custom function is not supported
"""
class AffinityPropagationClustering:
    def __init__(self):
        self.affinity_object = AffinityPropagation(affinity='euclidean')

    def fit_data(self, X):
        self.affinity_object.fit(X)

    def get_cluster_labels(self):
        return self.affinity_object.labels_

    def get_cluster_centers(self):
        return self.affinity_object.cluster_centers_

    def get_cluster_centers_indices(self):
        return self.affinity_object.cluster_centers_indices_

    def affinity_matrix(self):
        return self.affinity_object.affinity_matrix_

    def get_n_iterations(self):
        return self.affinity_object.n_iter_
