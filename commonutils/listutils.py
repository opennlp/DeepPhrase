
def get_unique_phrases(master_list, list_to_merge):
    tokenized_master_list = []
    unique_word_list = []
    for original_phrase in master_list:
        for word in original_phrase.split(" "):
            tokenized_master_list.append(word)
    for potential_merge_phrase in list_to_merge:
        phrase_count = 0
        for potential_word in potential_merge_phrase.split(" "):
            if potential_word not in tokenized_master_list:
                phrase_count += 1
        if phrase_count == len(potential_merge_phrase.split(" ")):
            unique_word_list.append(potential_merge_phrase)

    return unique_word_list


def sort_dict_by_values(unsorted_dict, top_n=7):
    sorted_by_value = sorted(unsorted_dict.items(), key=lambda kv: -kv[1])
    return sorted_by_value[:top_n]
