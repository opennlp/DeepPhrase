from sklearn.manifold import TSNE, LocallyLinearEmbedding, MDS
from sklearn.decomposition import PCA


def get_lower_dimensional_projection(cluster_data, algorithm='tsne' ,projection_dim=2):
    if algorithm.lower() == 'tsne':
        tsne_object = TSNE(n_components=projection_dim, random_state=42)
        lower_dimensional_projected_data = tsne_object.fit_transform(cluster_data)
        return lower_dimensional_projected_data
    elif algorithm.lower() == 'pca':
        pca_object = PCA(n_components=projection_dim, random_state=42, copy=False)
        lower_dimensional_projected_data = pca_object.fit_transform(cluster_data)
        return lower_dimensional_projected_data
    elif algorithm.lower() == "mds":
        mds_object = MDS(n_components=projection_dim, random_state=42)
        lower_dimensional_projected_data = mds_object.fit_transform(cluster_data)
        return lower_dimensional_projected_data
    else:
        lle_object = LocallyLinearEmbedding(n_components=projection_dim, random_state=42)
        lower_dimensional_projected_data = lle_object.fit_transform(cluster_data)
        return lower_dimensional_projected_data
