import time
import math
from concurrent import futures

import grpc

from data.data_load_module import load_data,build_feature_index, feature_index
from proto import similarity_pb2, similarity_pb2_grpc

SIMILARITY_SERVICE_ADDRESS = "[::]:8080"


def euclidean(a, b):
    s = 0.0
    for x, y in zip(a, b):
        d = x - y
        s += d * d
    return math.sqrt(s)


class SimilarityServicer(similarity_pb2_grpc.SimilarityServicer):
    def Find(self, request, context):
        query_vector = request.queryVector
        threshold = request.threshold

        image_ids = []

        for image_id, ref_vector in feature_index.items():
            dist = euclidean(query_vector, ref_vector)
            print(f"[SIM] {image_id} dist={dist:.4f}")
            if dist <= threshold:
                image_ids.append(image_id)

        return similarity_pb2.SimilarityResponse(
            imageIds=image_ids
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    similarity_pb2_grpc.add_SimilarityServicer_to_server(
        SimilarityServicer(), server
    )
    server.add_insecure_port(SIMILARITY_SERVICE_ADDRESS)
    load_data()
    build_feature_index()
    server.start()
    print("Similarity service running on 8080")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
