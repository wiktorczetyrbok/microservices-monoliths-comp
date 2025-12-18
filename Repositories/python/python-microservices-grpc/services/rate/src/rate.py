import time
from concurrent import futures
from dataclasses import dataclass
from typing import List

import grpc
from data.data_load_module import load_data, build_inventory_index, inventory_index
from proto import rate_pb2, rate_pb2_grpc

RATE_SERVICE_ADDRESS = "[::]:8080"


@dataclass
class RoomType:
    bookableRate: float
    code: str
    description: str
    totalRate: float
    totalRateInclusive: float


@dataclass
class RatePlan:
    hotelId: str
    code: str
    inDate: str
    outDate: str
    roomType: RoomType


@dataclass
class Result:
    ratePlans: List[RatePlan]


def get_rates(hotel_ids: List[str], in_date: str, out_date: str) -> Result:
    rate_plans = []
    for hotel_id in hotel_ids:
        rate_info = inventory_index.get(hotel_id, {}).get(in_date, {}).get(out_date)
        if rate_info:
            room_type_data = rate_info["roomType"]
            room_type = RoomType(**room_type_data)
            rate_plan = RatePlan(
                hotelId=hotel_id,
                code=rate_info["code"],
                inDate=in_date,
                outDate=out_date,
                roomType=room_type,
            )
            rate_plans.append(rate_plan)

    return Result(ratePlans=rate_plans)


def build_rate_proto_response(result):
    response = rate_pb2.Result()
    for ratePlan in result.ratePlans:
        rate_plan_proto = response.ratePlans.add()
        rate_plan_proto.hotelId = ratePlan.hotelId
        rate_plan_proto.code = ratePlan.code
        rate_plan_proto.inDate = ratePlan.inDate
        rate_plan_proto.outDate = ratePlan.outDate

        room_type_proto = rate_plan_proto.roomType
        room_type_proto.bookableRate = ratePlan.roomType.bookableRate
        room_type_proto.totalRate = ratePlan.roomType.totalRate
        room_type_proto.totalRateInclusive = ratePlan.roomType.totalRateInclusive
        room_type_proto.code = ratePlan.roomType.code
        room_type_proto.roomDescription = ratePlan.roomType.description

    return response


class RateServicer(rate_pb2_grpc.RateServicer):
    def GetRates(self, request, context):
        result = get_rates(request.hotelIds, request.inDate, request.outDate)
        return build_rate_proto_response(result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rate_pb2_grpc.add_RateServicer_to_server(RateServicer(), server)
    server.add_insecure_port(RATE_SERVICE_ADDRESS)
    load_data()
    build_inventory_index()
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
