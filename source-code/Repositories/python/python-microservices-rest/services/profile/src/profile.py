from flask import Flask, jsonify, request

from data.data_load_module import hotel_profiles_index

app = Flask(__name__)


def build_profile_response(matching_profiles):
    response_data = []
    for profile in matching_profiles:
        hotel_data = {
            "id": profile["id"],
            "name": profile["name"],
            "phoneNumber": profile["phoneNumber"],
            "description": profile["description"],
            "address": {
                "streetNumber": profile["address"]["streetNumber"],
                "streetName": profile["address"]["streetName"],
                "city": profile["address"]["city"],
                "state": profile["address"]["state"],
                "country": profile["address"]["country"],
                "postalCode": profile["address"]["postalCode"],
                "lat": profile["address"]["lat"],
                "lon": profile["address"]["lon"],
            },
        }
        response_data.append(hotel_data)
    return response_data


@app.route("/profile", methods=["GET"])
def get_profiles():
    hotel_ids = [hotel_id for hotel_id in request.args.getlist("hotelIds")]
    matching_profiles = [
        hotel_profiles_index.get(hotel_id)
        for hotel_id in hotel_ids
        if hotel_id in hotel_profiles_index
    ]
    if not matching_profiles:
        return []

    response_data = build_profile_response(matching_profiles)

    return jsonify(response_data)
