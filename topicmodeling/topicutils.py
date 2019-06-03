from topicmodeling import generic_lda
from gensim.summarization import keywords
import numpy as np
from wordvectorizer import embedding
from clusterwrapper.clustering import KMeansClustering, DBSCANClustering, AffinityPropagationClustering
from commonutils import dimensionreductionutils, visualutils


def get_lda_topic_map(text_list, topic_num, ngram_value, channel_name='reddit', iteration_num=1, embedding_algorithm='glove', visualize_topic=False):
    filename_to_save = "_".join([channel_name,embedding_algorithm,str(ngram_value), str(iteration_num)]) + ".html"
    html_data, topic_list, coherence_score = generic_lda.get_formatted_html_data(text_list, num_topics=topic_num, ngram_value=ngram_value)
    topic_map = dict({})

    if visualize_topic:
        try:
            with open(filename_to_save, 'x') as f:
                f.write(html_data)
        except Exception:
            pass

    for topic_tuple in topic_list:
        topic_number = topic_tuple[0]
        topic_specific_word_list = topic_tuple[1]
        topic_word_list = list([])
        for topic_word_tuple in topic_specific_word_list:
            topic_word_list.append(topic_word_tuple[0])
        topic_map[topic_number] = topic_word_list
    return topic_map, coherence_score


def extract_keyphrase_list(text_string,ratio=0.5,min_phrase_length=1):
    keyword_list = keywords(text_string, ratio=ratio, split=True, scores=True,lemmatize=True)
    scale = 25.0
    filtered_keyword_list = list([])
    for keyword_tuple in keyword_list:
        keyword = keyword_tuple[0].lower().strip()
        if len(keyword.split(' ')) >= min_phrase_length:
            filtered_keyword_list.append(keyword)
    return filtered_keyword_list


def get_cluster_dict(text_list,num_clusters,cluster_algo='kmeans',embedding_algorithm='glove',channel_name="reddit", ngram=3, iteration=1, plot_clusters=False):
    text_list_embedding_matrix = np.array(embedding.get_word_embeddings(text_list,model_to_use=embedding_algorithm))
    if cluster_algo.lower() == 'dbscan':
        cluster_object = DBSCANClustering()
    elif cluster_algo.lower() == 'affinitypropagation':
        cluster_object = AffinityPropagationClustering()
    else:
        cluster_object = KMeansClustering(n_clusters=num_clusters)
    cluster_object.fit_data(text_list_embedding_matrix)
    cluster_label_list = cluster_object.get_cluster_labels()
    cluster_label_text_dict = dict({})
    if plot_clusters:
        plot_clusters_per_iteration(text_list_embedding_matrix,cluster_label_list,
                                    channel_name=channel_name,
                                    algorithm_name=embedding_algorithm,
                                    ngram_value=ngram,
                                    iteration_num=iteration)

    silhouette_coefficient = cluster_object.get_silhouette_score(text_list_embedding_matrix)
    calinski_harabiz_index = cluster_object.get_calinski_harabiz_score(text_list_embedding_matrix)
    for i in range(num_clusters):
        cluster_label_text_dict[i] = list([])
    for cluster_text_index, cluster_label_number in enumerate(cluster_label_list):
        cluster_text_list = cluster_label_text_dict[cluster_label_number]
        cluster_text_list.append(text_list[cluster_text_index])
        cluster_label_text_dict[cluster_label_number] = cluster_text_list
    return cluster_label_text_dict, silhouette_coefficient, calinski_harabiz_index


def plot_clusters_per_iteration(text_list_embedding_matrix, cluster_label_list, channel_name,algorithm_name,ngram_value,iteration_num):
    filename_to_persist = "_".join([channel_name, algorithm_name, str(ngram_value), str(iteration_num)]) + ".png"
    lower_dimensional_projection = dimensionreductionutils.get_lower_dimensional_projection(text_list_embedding_matrix)
    visualize_cluster_object = visualutils.VisualizeClusters(lower_dimensional_projection[:, 0],
                                                             lower_dimensional_projection[:, 1], cluster_label_list)
    visualize_cluster_object.plot_scatter_chart(x_label="First Dimension", y_label="Second Dimension",
                                                title="Visualzation of Cluster", filename_to_save=filename_to_persist, show_plot=False)