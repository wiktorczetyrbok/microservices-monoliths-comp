import time
from concurrent import futures

import grpc
from data.data_load_module import (
    load_data,
    metadata_index,
)
from proto import metadata_pb2, metadata_pb2_grpc

METADATA_SERVICE_ADDRESS = "[::]:8080"


class MetadataServicer(metadata_pb2_grpc.MetadataServicer):

    def Get(self, request, context):
        response = metadata_pb2.MetadataResponse()
        for image_id in request.imageIds:
            meta = metadata_index.get(image_id)
            if meta:
                image = response.images.add()
                image.id = meta["id"]
                image.name = meta["name"]
                image.tags.extend(meta["tags"])

        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    metadata_pb2_grpc.add_MetadataServicer_to_server(
        MetadataServicer(), server
    )
    server.add_insecure_port(METADATA_SERVICE_ADDRESS)
    load_data()

    server.start()
    print("Metadata service running on 8080")

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
