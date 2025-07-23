from dataclasses import dataclass
from typing import List

from flask import Flask, jsonify, request

from data.data_load_module import inventory_index

app = Flask(__name__)


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


def get_rates(hotel_ids, in_date, out_date):
    rate_plans = []
    for hotel_id in hotel_ids:
        rate_info = inventory_index.get(hotel_id, {}).get(in_date, {}).get(out_date)
        if rate_info:
            rate_plan_data = {
                'hotelId': hotel_id,
                'code': rate_info["code"],
                'inDate': in_date,
                'outDate': out_date,
                'roomType': rate_info["roomType"]
            }
            rate_plans.append(rate_plan_data)

    return rate_plans


@app.route('/rate', methods=['POST'])
def get_rates_endpoint():
    data = request.json
    hotel_ids = data['hotelIds']
    in_date = data['inDate']
    out_date = data['outDate']

    rate_plans = get_rates(hotel_ids, in_date, out_date)
    return jsonify(rate_plans)
