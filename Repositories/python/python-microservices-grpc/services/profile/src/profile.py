import time
from concurrent import futures

import grpc
from data.data_load_module import (
    load_data,
    build_hotel_profiles_index,
    hotel_profiles_index,
)
from proto import profile_pb2, profile_pb2_grpc

PROFILE_SERVICE_ADDRESS = "[::]:8080"


def build_profile_proto_response(matching_profiles):
    result = profile_pb2.Result()
    for profile in matching_profiles:
        hotel = result.hotels.add()
        hotel.id = profile["id"]
        hotel.name = profile["name"]
        hotel.phoneNumber = profile["phoneNumber"]
        hotel.description = profile["description"]

        address = profile["address"]
        hotel.address.streetNumber = address["streetNumber"]
        hotel.address.streetName = address["streetName"]
        hotel.address.city = address["city"]
        hotel.address.state = address["state"]
        hotel.address.country = address["country"]
        hotel.address.postalCode = address["postalCode"]
        hotel.address.lat = address["lat"]
        hotel.address.lon = address["lon"]

    return result


class ProfileServicer(profile_pb2_grpc.ProfileServicer):
    def GetProfiles(self, request, context):
        matching_profiles = [
            hotel_profiles_index.get(hotel_id)
            for hotel_id in request.hotelIds
            if hotel_id in hotel_profiles_index
        ]
        if not matching_profiles:
            return []

        return build_profile_proto_response(matching_profiles)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    profile_pb2_grpc.add_ProfileServicer_to_server(ProfileServicer(), server)
    server.add_insecure_port(PROFILE_SERVICE_ADDRESS)
    load_data()
    build_hotel_profiles_index()
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
