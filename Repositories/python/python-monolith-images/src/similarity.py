import math
from src.data_load_module import feature_index


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def find_similar_images(query_vector, threshold):
    matches = []

    for image_id, ref_vector in feature_index.items():
        distance = euclidean(query_vector, ref_vector)
        if distance <= threshold:
            matches.append(image_id)

    return matches
