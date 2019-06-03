from scipy import stats
import numpy as np


def convert_fraction_into_percentages(data_list):
    total = np.sum(data_list)
    for index, data in enumerate(data_list):
        data_list[index] = (data_list[index]/total)*100.0
    return data_list


def get_modal_value(data_list):
    return stats.mode(data_list)[0][0]


def get_data_distribution(data_list):
    data_dict = dict({})
    for data_value in data_list:
        index_str = str(data_value)
        if index_str in data_dict.keys():
            data_dict[index_str] = data_dict[index_str] + 1.0
        else:
            data_dict[index_str] = 1.0
    total_sum = sum(data_dict.values())
    for key, value in data_dict.items():
        data_dict[key] = (value/total_sum) * 100.0
    return data_dict

