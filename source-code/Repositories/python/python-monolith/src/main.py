import logging

from flask import Flask, request, jsonify, abort

from src.geo import get_nearby_hotels
from src.profile import get_hotel_profiles
from src.rate import get_rates

app = Flask(__name__)


@app.route("/hotels", methods=["GET"])
def get_hotels():
    try:
        logging.info("Main application starting")
        # Parse the HTTP request
        in_date = request.args.get("inDate")
        out_date = request.args.get("outDate")
        lat = float(request.args.get("lat", 0))
        lon = float(request.args.get("lon", 0))
        if not in_date or not out_date:
            abort(400, description="Invalid date parameters")

        # Call the geo function
        nearby_hotel_ids = get_nearby_hotels(lat, lon)
        if not nearby_hotel_ids:
            logging.error("No hotels found in 10 km radius of given point.")
            return jsonify([])

        # Fetch rate information
        rate_results = get_rates(nearby_hotel_ids, in_date, out_date)
        if not rate_results:
            logging.error("No hotels found for given location and dates.")
            return jsonify([])

        # Using only the hotel IDs for the profile service
        rate_hotel_ids = [ratePlan.hotelId for ratePlan in rate_results.ratePlans]

        # Call the profile function
        profile_results = get_hotel_profiles(rate_hotel_ids)

        # Convert the REST API response to a desired JSON format
        hotels = [
            {
                "type": "Feature",
                "id": hotel["id"],
                "properties": {
                    "name": hotel["name"],
                    "phone_number": hotel["phoneNumber"],
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [hotel["address"]["lat"], hotel["address"]["lon"]],
                },
            }
            for hotel in profile_results
        ]
        return jsonify(hotels)

    except ValueError:
        abort(400, description="Invalid latitude or longitude")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        abort(500, description="Internal Server Error")

