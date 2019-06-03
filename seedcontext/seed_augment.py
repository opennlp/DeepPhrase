from topicmodeling import topicutils
from twitterfetch import twittersearch
from newsfetch import searchnews
from redditfetch import redditsearch
from wordvectorizer import embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from commonutils import statutils, listutils, dbutils, logutils
from benchmark import query_augment
from topicmodeling.generic_lda import get_ngram_count_dict
from constants import modelconstants
from persistence import storage_handler

LOGGER = logutils.get_logger("Seed Augment")


class IterativeQueryAugment:
    def __init__(self, seed_phrase_list, intent_word_dict, num_iterations=10):
        self.seed_phrase_list = seed_phrase_list
        self.intent_word_dict = intent_word_dict
        self.num_iterations = num_iterations

    def get_data_list(self, data_source="twitter"):
        master_result_list = []
        if data_source.lower() == "news":
            news_fetch_object = searchnews.News()
            for query_phrase in self.seed_phrase_list:
                result_list = news_fetch_object.get_data(query_phrase)
                for index, result_dict in enumerate(result_list):
                    result_list[index] = result_dict['description']
                master_result_list.extend(result_list)
        elif data_source.lower() == "reddit":
            reddit_fetch_object = redditsearch.Reddit()
            for query_phrase in self.seed_phrase_list:
                result_list = reddit_fetch_object.get_data(query_phrase)
                for index, result_dict in enumerate(result_list):
                    result_list[index] = result_dict['title']
                master_result_list.extend(result_list)
        else:
            twitter_fetch_object = twittersearch.Twitter()
            for query_phrase in self.seed_phrase_list:
                result_list = twitter_fetch_object.get_data(query_phrase)
                for index, result_dict in enumerate(result_list):
                    result_list[index] = result_dict['text']
                master_result_list.extend(result_list)
        return master_result_list

    def get_cluster_map(self, result_text_list, embedding_model='glove',clustering_algorithm="lda", ngram_value=3, data_source="reddit", iteration=1):
        topic_number = len(self.intent_word_dict.keys())
        if clustering_algorithm.lower() == 'none':
            return dict({0: result_text_list})
        elif clustering_algorithm.lower() == "kmeans":
            return topicutils.get_cluster_dict(result_text_list,
                                               num_clusters=topic_number,
                                               cluster_algo='kmeans',
                                               embedding_algorithm=embedding_model,
                                               channel_name=data_source,
                                               ngram=ngram_value,
                                               iteration=iteration)
        else:
            return topicutils.get_lda_topic_map(result_text_list,
                                                topic_num=topic_number,
                                                ngram_value=ngram_value,
                                                channel_name=data_source,
                                                iteration_num=iteration,
                                                embedding_algorithm=embedding_model)

    @staticmethod
    def get_word_embedding_list(text_list, embedding_algorithm="glove"):
        return embedding.get_word_embeddings(text_list, model_to_use=embedding_algorithm)

    @staticmethod
    def update_intent_dictionary(previous_intention_dict, current_intention_dict):
        for intent_name in current_intention_dict.keys():
            for intent_keyphrase in current_intention_dict[intent_name]:
                if intent_keyphrase not in previous_intention_dict[intent_name]:
                    intent_specific_list = previous_intention_dict[intent_name]
                    intent_specific_list.append(intent_keyphrase)
                    previous_intention_dict[intent_name] = intent_specific_list
        return previous_intention_dict

    def get_initialized_intent_dict(self):
        master_intent_keyword_dict = dict({})
        for intent_name in self.intent_word_dict.keys():
            master_intent_keyword_dict[intent_name] = list([])
        return master_intent_keyword_dict

    @staticmethod
    def get_similarity(word_embedding_matrix, intent_embedding_matrix, similarity_measure='cosine'):
        if similarity_measure.lower() == 'cosine':
            return cosine_similarity(intent_embedding_matrix, word_embedding_matrix)

    def get_cluster_similarity_matrix(self, text_list, embedding_algorithm="glove", similarity_measure='cosine'):
        intent_list = []
        for intent_phrase in self.intent_word_dict.values():
            intent_list.append(intent_phrase)
        cluster_topic_embedding_matrix = np.array(self.get_word_embedding_list(text_list, embedding_algorithm=embedding_algorithm))
        intent_embedding_matrix = np.array(self.get_word_embedding_list(intent_list, embedding_algorithm=embedding_algorithm))
        return self.get_similarity(cluster_topic_embedding_matrix, intent_embedding_matrix, similarity_measure=similarity_measure)

    def get_top_n_matching_phrases(self, intent_phrase, potential_word_list, model_to_use="glove", similarity_measure='cosine'):
        intent_embedding = np.array(embedding.get_word_embeddings([intent_phrase], model_to_use=model_to_use)[0]).reshape(1, -1)
        potential_word_embedding = np.array(embedding.get_word_embeddings(potential_word_list, model_to_use=model_to_use))
        pairwise_similarity_list = list(self.get_similarity(potential_word_embedding, intent_embedding, similarity_measure=similarity_measure)[0])
        word_similarity_dict = dict({})
        for potential_index, potential_word in enumerate(potential_word_list):
            word_similarity_dict[potential_word] = pairwise_similarity_list[potential_index]
        top_n_word_distance_tuple = listutils.sort_dict_by_values(word_similarity_dict,top_n=10)
        top_n_matching_phrase_list = []
        for word_tuple in top_n_word_distance_tuple:
            top_n_matching_phrase_list.append(word_tuple[0])
        return top_n_matching_phrase_list


def generate_iterative_seed(channel_name, seed_phrase_list, intent_dict, num_iterations=10,cluster_algorithm='lda',
                            ngram_value=2, embedding_model='glove', similarity_measure='cosine', storage_type=modelconstants.DB_STORAGE_TYPE):

    query_batch_iterator_driver = IterativeQueryAugment(seed_phrase_list, intent_dict, num_iterations=num_iterations)

    metadata = dict({'channel': channel_name,
                     'seed_phrase_list': seed_phrase_list,
                     'intent_dict': intent_dict,
                     'num_iterations': num_iterations,
                     'cluster_algorithm': cluster_algorithm,
                     'ngram_value': ngram_value,
                     'embedding_model': embedding_model,
                     'similarity_measure': similarity_measure})

    seed_word_size = len(seed_phrase_list)
    storage_connector = storage_handler.StorageHandler(storage_type=storage_type)
    master_intent_word_dictionary = query_batch_iterator_driver.get_initialized_intent_dict()

    for i in range(num_iterations):

        # Initializing the batch log object
        batch_log = query_augment.QueryBatchMetric(iteration=i+1,metadata=metadata)

        # Fetching data list from source
        text_data_list = query_batch_iterator_driver.get_data_list(data_source=channel_name)

        LOGGER.info("Data fetched from %s" % channel_name)

        # Storing the data for log purposes
        batch_log.results_fetched = text_data_list
        batch_log.number_results = len(text_data_list)

        # Getting Clustered topics and setting the topic scores for lda and clusters
        if cluster_algorithm.lower() == "kmeans":
            cluster_word_list_dict, silhouette_score, calinski_harabiz_index = query_batch_iterator_driver.get_cluster_map(text_data_list,
                                                                                                                           clustering_algorithm=cluster_algorithm,
                                                                                                                           ngram_value=ngram_value,
                                                                                                                           data_source=channel_name,
                                                                                                                           iteration=i+1,
                                                                                                                           embedding_model=embedding_model)

            batch_log.cluster_metric = {'silhouette': silhouette_score,
                                        'calinski_harabiz': calinski_harabiz_index}
            print(batch_log.cluster_metric)

        elif cluster_algorithm.lower() == "lda":
            cluster_word_list_dict, coherence_score = query_batch_iterator_driver.get_cluster_map(text_data_list,
                                                                                                  clustering_algorithm=cluster_algorithm,
                                                                                                  ngram_value=ngram_value,
                                                                                                  data_source=channel_name,
                                                                                                  iteration=i+1,
                                                                                                  embedding_model=embedding_model)
            batch_log.cluster_coherence = coherence_score
            print(batch_log.cluster_coherence)
        else:
            cluster_word_list_dict = query_batch_iterator_driver.get_cluster_map(text_data_list, clustering_algorithm=cluster_algorithm, ngram_value=ngram_value)

        LOGGER.info("Cluster Metrics Initialized for %s" % str(cluster_algorithm))

        # Get intent name list
        intent_name_list = list(query_batch_iterator_driver.intent_word_dict.keys())

        # Get cluster word list
        master_cluster_word_list = list(cluster_word_list_dict.values())

        extracted_topic_word_list_dict = dict({})

        # Initializing cluster purity dict
        per_cluster_purity_dict = dict({})

        # Initializing the extracted word dictionary
        for intent_name in intent_name_list:
            extracted_topic_word_list_dict[intent_name] = list([])

        # Matching the clustered keyphrases with the intents
        for cluster_index, topic_word_list in enumerate(master_cluster_word_list):
            intent_topic_similarity_matrix = query_batch_iterator_driver.get_cluster_similarity_matrix(topic_word_list,
                                                                                                       embedding_algorithm=embedding_model,
                                                                                                       similarity_measure=similarity_measure)
            topic_index_vector = list(np.argmax(intent_topic_similarity_matrix, axis=0))
            per_cluster_purity_dict[str(cluster_index)] = statutils.get_data_distribution(topic_index_vector)

            for topic_word_index, topic_number in enumerate(topic_index_vector):
                extracted_topic_list = extracted_topic_word_list_dict[intent_name_list[topic_number]]
                extracted_topic_list.append(topic_word_list[topic_word_index])
                extracted_topic_word_list_dict[intent_name_list[topic_number]] = extracted_topic_list

        # Storing all intent matching keyphrases
        batch_log.intent_keyphrase_dict = extracted_topic_word_list_dict

        # Storing cluster purity
        batch_log.cluster_purity = per_cluster_purity_dict

        LOGGER.info("Topic Word Dict Initialized for %s " % str(cluster_algorithm))

        # Finding top-n matching phrases for each intent
        top_matching_word_by_intent_dict = dict({})
        for intent_phrase_name, extracted_word_list in extracted_topic_word_list_dict.items():
            if cluster_algorithm.lower() == "none" or cluster_algorithm.lower() == "kmeans":
                ngrams_list = get_ngram_count_dict(extracted_word_list,ngram_value=ngram_value).keys()

                top_n_matching_list = query_batch_iterator_driver.get_top_n_matching_phrases(intent_phrase_name,
                                                                                             ngrams_list,
                                                                                             model_to_use=embedding_model,
                                                                                             similarity_measure=similarity_measure)
            else:
                top_n_matching_list = query_batch_iterator_driver.get_top_n_matching_phrases(intent_phrase_name,
                                                                                             extracted_word_list,
                                                                                             model_to_use=embedding_model,
                                                                                             similarity_measure=similarity_measure)
            top_matching_word_by_intent_dict[intent_phrase_name] = top_n_matching_list

        updated_seed_word_list = list([])
        initial_seed_word_list = query_batch_iterator_driver.seed_phrase_list[:seed_word_size]

        # Storing Top Intent Match Phrases
        batch_log.intent_top_keyphrase_dict = top_matching_word_by_intent_dict
        master_intent_word_dictionary = query_batch_iterator_driver.update_intent_dictionary(master_intent_word_dictionary, batch_log.intent_top_keyphrase_dict)
        print(master_intent_word_dictionary)

        # Finding Top-K Non Overlapping keywords
        for intent_phrase_name, top_selected_word_list in top_matching_word_by_intent_dict.items():
            unique_word_list = listutils.get_unique_phrases(query_batch_iterator_driver.seed_phrase_list,top_selected_word_list)
            for unique_word in unique_word_list:
                for seed_word in initial_seed_word_list:
                    updated_seed_word_list.append(seed_word + " " + unique_word)

        # Storing updated seed
        batch_log.updated_keyphrase_list = updated_seed_word_list

        # Appending the updated seed phrase list to the initial list
        original_seed_phrase_list = query_batch_iterator_driver.seed_phrase_list
        original_seed_phrase_list.extend(updated_seed_word_list)
        query_batch_iterator_driver.seed_phrase_list = original_seed_phrase_list
        LOGGER.info("Keyword List Extracted")
        print(batch_log.updated_keyphrase_list)
        print(batch_log.cluster_purity)
        # Inserting the metrics in database
        storage_connector.persist_data(batch_log.get_object_dict())

    storage_connector.close_connection()
    return master_intent_word_dictionary
