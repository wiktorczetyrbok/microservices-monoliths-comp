import time
from concurrent import futures
import grpc

from data.data_load_module import load_data, image_buffers
from proto import feature_pb2, feature_pb2_grpc
from src.extract import extract_features


FEATURE_SERVICE_ADDRESS = "[::]:8080"


class FeatureServicer(feature_pb2_grpc.FeatureServicer):

    def Extract(self, request, context):
        image_id = request.imageId
        kernel = request.kernel
        print("request in FeatureService: ", request)
        buffer = image_buffers.get(image_id)
        if buffer is None:
            return feature_pb2.FeatureResponse(vector=[])

        vector = extract_features(buffer, kernel)

        return feature_pb2.FeatureResponse(vector=vector)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    feature_pb2_grpc.add_FeatureServicer_to_server(
        FeatureServicer(), server
    )

    server.add_insecure_port(FEATURE_SERVICE_ADDRESS)

    load_data()

    server.start()
    print("[FEATURE] service running on 8080")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
