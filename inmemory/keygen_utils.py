
def get_unique_mapping_key(data_dict):
    metadata_dict = data_dict['metadata']
    unique_key_value = metadata_dict['channel'] + '_' + metadata_dict['cluster_algorithm'] + '_' + \
                       str(metadata_dict['ngram_value']) + '_' + metadata_dict['embedding_model'] + '_' + metadata_dict['similarity_measure']
    return unique_key_value
