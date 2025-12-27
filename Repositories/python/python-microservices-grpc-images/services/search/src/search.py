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

        self.feature_stub = feature_pb2_grpc.FeatureStub(
            self.feature_channel
        )
        self.similarity_stub = similarity_pb2_grpc.SimilarityStub(
            self.similarity_channel
        )

    def Search(self, request, context):
        feature_response = self.feature_stub.Extract(
            feature_pb2.FeatureRequest(
                imageId="img001",
                kernel=request.kernel,
            )
        )

        similarity_response = self.similarity_stub.Find(
            similarity_pb2.SimilarityRequest(
                queryVector=feature_response.vector,
                threshold=request.threshold,
            )
        )
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

    print("Search service running on 8080")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
