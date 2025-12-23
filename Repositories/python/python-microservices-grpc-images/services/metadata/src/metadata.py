import time
from concurrent import futures

import grpc
from data.data_load_module import (
    load_data,
    build_metadata_index,
    metadata_index,
)
from proto import metadata_pb2, metadata_pb2_grpc

METADATA_SERVICE_ADDRESS = "[::]:8080"


def build_metadata_proto_response(matching_metadata):
    result = metadata_pb2.MetadataResponse()
    for meta in matching_metadata:
        image = result.images.add()
        image.id = meta["id"]
        image.name = meta["name"]
        image.tags.extend(meta["tags"])
    return result


class MetadataServicer(metadata_pb2_grpc.MetadataServicer):
    def Get(self, request, context):
        matching_metadata = [
            metadata_index.get(image_id)
            for image_id in request.imageIds
            if image_id in metadata_index
        ]

        if not matching_metadata:
            return metadata_pb2.MetadataResponse()

        return build_metadata_proto_response(matching_metadata)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    metadata_pb2_grpc.add_MetadataServicer_to_server(
        MetadataServicer(), server
    )
    server.add_insecure_port(METADATA_SERVICE_ADDRESS)
    load_data()
    build_metadata_index()
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
