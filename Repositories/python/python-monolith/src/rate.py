from dataclasses import dataclass
from typing import List

from src.data_load_module import inventory_index


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
            room_type_data = rate_info['roomType']
            room_type = RoomType(**room_type_data)
            rate_plan = RatePlan(
                hotelId=hotel_id,
                code=rate_info['code'],
                inDate=in_date,
                outDate=out_date,
                roomType=room_type
            )
            rate_plans.append(rate_plan)

    return Result(ratePlans=rate_plans)
