import logging

import grpc
from flask import Flask, request, jsonify, abort
from proto import profile_pb2, profile_pb2_grpc
from proto import search_pb2, search_pb2_grpc

app = Flask(__name__)

SEARCH_SERVICE_ADDRESS = 'search:8080'
PROFILE_SERVICE_ADDRESS = 'profile:8080'


@app.route('/hotels', methods=['GET'])
def get_hotels():
    try:
        logging.info("Gateway service starting")
        # Parse the HTTP request
        in_date = request.args.get("inDate")
        out_date = request.args.get("outDate")
        lat = float(request.args.get("lat", 0))
        lon = float(request.args.get("lon", 0))
        if not in_date or not out_date:
            abort(400, description="Invalid date parameters")

        # Call the search service using gRPC
        with grpc.insecure_channel(SEARCH_SERVICE_ADDRESS) as channel:
            stub = search_pb2_grpc.SearchStub(channel)
            search_response = stub.Nearby(search_pb2.NearbyRequest(lat=lat, lon=lon, inDate=in_date, outDate=out_date))

        hotel_ids = search_response.hotelIds
        if not hotel_ids:
            logging.info("No hotels found for the given location and dates.")
            return jsonify([])

        # Call the profile service using gRPC
        with grpc.insecure_channel(PROFILE_SERVICE_ADDRESS) as channel:
            stub = profile_pb2_grpc.ProfileStub(channel)
            profile_response = stub.GetProfiles(profile_pb2.Request(hotelIds=hotel_ids))

        # Convert the gRPC response to a JSON-friendly format
        hotels = [
            {'type': 'Feature', 'id': hotel.id, 'properties': {'name': hotel.name, 'phone_number': hotel.phoneNumber},
             'geometry': {'type': 'Point', 'coordinates': [hotel.address.lat, hotel.address.lon]}} for hotel in
            profile_response.hotels]

        return jsonify(hotels)

    except grpc.RpcError as e:
        logging.error(f"An error occurred while calling gRPC service: {e}")
        return jsonify({'error': 'Service unavailable'}), 503
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'Internal server error'}), 500
