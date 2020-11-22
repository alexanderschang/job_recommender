import re
import math
from collections import Counter

# Computes the cosine similarity scores


class CosineSimilarity:
    def __init__(self):
        print('Cosine Similarity initialized')

    @staticmethod
    def cosine_similarity_of(text1, text2):
        first = re.compile(r"[\w']+").findall(str(text1))
        second = re.compile(r"[\w']+").findall(str(text2))
        vector1 = Counter(first)
        vector2 = Counter(second)

        common = set(vector1.keys()).intersection(set(vector2.keys()))
        dot_product = 0.0

        for i in common:
            dot_product += vector1[i] * vector2[i]

        squared_sum_vector1 = 0.0
        squared_sum_vector2 = 0.0

        for i in vector1.keys():
            squared_sum_vector1 += vector1[i]**2

        for i in vector2.keys():
            squared_sum_vector2 += vector2[i]**2

        magnitude = math.sqrt(squared_sum_vector1) * \
            math.sqrt(squared_sum_vector2)

        if not magnitude:
            return 0.0
        else:
            return float(dot_product) / magnitude
