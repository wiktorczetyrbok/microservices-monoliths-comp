import logging
import grpc
from flask import Flask, request, jsonify

from proto import search_pb2, search_pb2_grpc
from proto import metadata_pb2, metadata_pb2_grpc

app = Flask(__name__)

SEARCH_SERVICE_ADDRESS = 'search:8080'
METADATA_SERVICE_ADDRESS = 'metadata:8080'


@app.route('/images/search', methods=['GET'])
def search_images():
    try:
        logging.info("Image gateway request received")

        kernel = int(request.args.get("kernel", 3))
        threshold = float(request.args.get("threshold", 0.9))

        # ---- Search service ----
        with grpc.insecure_channel(SEARCH_SERVICE_ADDRESS) as channel:
            stub = search_pb2_grpc.SearchStub(channel)
            search_response = stub.Search(
                search_pb2.SearchRequest(
                    kernel=kernel,
                    threshold=threshold
                )
            )

        image_ids = search_response.imageIds
        if not image_ids:
            return jsonify([])

        # ---- Metadata service ----
        with grpc.insecure_channel(METADATA_SERVICE_ADDRESS) as channel:
            stub = metadata_pb2_grpc.MetadataStub(channel)
            metadata_response = stub.Get(
                metadata_pb2.MetadataRequest(
                    imageIds=image_ids
                )
            )

        images = [
            {
                "id": img.id,
                "name": img.name,
                "tags": list(img.tags)
            }
            for img in metadata_response.images
        ]

        return jsonify(images)

    except grpc.RpcError as e:
        logging.error(f"gRPC error: {e}")
        return jsonify({'error': 'Service unavailable'}), 503
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
