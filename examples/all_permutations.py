from seedcontext import seed_augment
from commonutils import logutils
from periodicschedule import scheduleupdate
from constants import modelconstants

LOGGER = logutils.get_logger('All Permutation Example')


def example_all_combinations():
    channel_name_list = ["news", "reddit", "twitter"]
    seed_phrase_list = ["adobe photoshop"]
    intent_dict = dict({'design': "design creative",
                        "image": "edit layer filter image",
                        "photography": "photography tool"})
    cluster_algorithm_list = ["none", "kmeans", "lda"]
    embedding_model_list = ["glove", "word2vec", "fasttext", "universalencoder"]
    storage_type_list = [modelconstants.DB_STORAGE_TYPE, modelconstants.INMEMORY_STORAGE_TYPE, modelconstants.QUEUE_STORAGE_TYPE]

    ngram_value = 3
    num_iterations = 7
    similarity_measure = 'cosine'

    for channel_name in channel_name_list:
        for clustering_algorithm in cluster_algorithm_list:
            for embedding_model in embedding_model_list:
                for storage_type in storage_type_list:
                    try:
                        seed_augment.generate_iterative_seed(channel_name=channel_name,
                                                seed_phrase_list=seed_phrase_list,
                                                intent_dict=intent_dict,
                                                num_iterations=num_iterations,
                                                ngram_value=ngram_value,
                                                cluster_algorithm=clustering_algorithm,
                                                embedding_model=embedding_model,
                                                similarity_measure=similarity_measure,
                                                storage_type=storage_type)
                    except Exception as e:
                        LOGGER.info("An exception occurred in seed augment")
                        print(str(e))


if __name__ == '__main__':
    scheduleupdate.update_scheduler(example_all_combinations, time_quantum_unit='seconds', time_quantum=1)
