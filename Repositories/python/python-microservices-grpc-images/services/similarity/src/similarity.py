import time
from concurrent import futures
import math

import grpc
from data.data_load_module import load_data, build_feature_index, feature_index
from proto import similarity_pb2, similarity_pb2_grpc

SIMILARITY_SERVICE_ADDRESS = "[::]:8080"


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def find_similar_images(query_vector, threshold):
    image_ids = []
    for image_id, ref_vector in feature_index.items():
        distance = euclidean(query_vector, ref_vector)
        if distance <= threshold:
            image_ids.append(image_id)
    return image_ids


def build_similarity_proto_response(image_ids):
    response = similarity_pb2.SimilarityResponse()
    response.imageIds.extend(image_ids)
    return response


class SimilarityServicer(similarity_pb2_grpc.SimilarityServicer):
    def Find(self, request, context):
        image_ids = find_similar_images(
            request.queryVector,
            request.threshold
        )
        return build_similarity_proto_response(image_ids)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    similarity_pb2_grpc.add_SimilarityServicer_to_server(
        SimilarityServicer(), server
    )
    server.add_insecure_port(SIMILARITY_SERVICE_ADDRESS)
    load_data()
    build_feature_index()
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
