import time
from concurrent import futures

import grpc
from proto import feature_pb2, feature_pb2_grpc
from proto import similarity_pb2, similarity_pb2_grpc
from proto import search_pb2, search_pb2_grpc

SEARCH_SERVICE_ADDRESS = "[::]:8080"
FEATURE_SERVICE_ADDRESS = "feature:8080"
SIMILARITY_SERVICE_ADDRESS = "similarity:8080"


class SearchServicer(search_pb2_grpc.SearchServicer):
    def __init__(self):
        self.feature_channel = grpc.insecure_channel(FEATURE_SERVICE_ADDRESS)
        self.similarity_channel = grpc.insecure_channel(
            SIMILARITY_SERVICE_ADDRESS
        )

    def Search(self, request, context):
        feature_stub = feature_pb2_grpc.FeatureStub(self.feature_channel)

        feature_request = feature_pb2.FeatureRequest(
            imageId="img001",
            kernel=request.kernel,
        )
        feature_response = feature_stub.Extract(feature_request)

        similarity_stub = similarity_pb2_grpc.SimilarityStub(
            self.similarity_channel
        )
        similarity_request = similarity_pb2.SimilarityRequest(
            queryVector=feature_response.vector,
            threshold=request.threshold,
        )
        similarity_response = similarity_stub.Find(similarity_request)

        return search_pb2.SearchResponse(
            imageIds=similarity_response.imageIds
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    search_pb2_grpc.add_SearchServicer_to_server(
        SearchServicer(), server
    )
    server.add_insecure_port(SEARCH_SERVICE_ADDRESS)
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
