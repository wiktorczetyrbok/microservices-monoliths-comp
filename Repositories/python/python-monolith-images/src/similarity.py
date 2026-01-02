import math
from src.data_load_module import feature_index


def euclidean(a, b):
    s = 0.0
    for x, y in zip(a, b):
        d = x - y
        s += d * d
    return math.sqrt(s)


def find_similar_images(query_vector, threshold):
    result = []
    for image_id, ref in feature_index.items():
        dist = euclidean(query_vector, ref)
        print(f"[SIM] {image_id} dist={dist:.4f}")
        if dist <= threshold:
            result.append(image_id)
    return result
