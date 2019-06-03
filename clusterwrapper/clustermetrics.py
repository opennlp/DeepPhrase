from sklearn.metrics import silhouette_score, calinski_harabaz_score


def get_silhouette_coefficient(cluster_train_data,labels_assigned):
    return silhouette_score(cluster_train_data,labels_assigned)


def get_calinski_harabaz_coefficient(cluster_train_data, labels_assigned):
    return calinski_harabaz_score(cluster_train_data, labels_assigned)