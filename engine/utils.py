import numpy as np
import math


def calculate_tf(f_td):
    tf = 1 + np.log10(f_td)
    return tf


def vector_length(vector_dict):
    length = math.sqrt(sum(tf_idf_value['tf'] ** 2 for tf_idf_value in vector_dict.values()))
    return length
