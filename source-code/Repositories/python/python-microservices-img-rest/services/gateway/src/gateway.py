import logging

import requests
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

SEARCH_SERVICE_URL = 'http://search:8080/search'
PROFILE_SERVICE_URL = 'http://profile:8080/profile'


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

        # Call the search service
        search_payload = {
            "lat": lat,
            "lon": lon,
            "inDate": in_date,
            "outDate": out_date
        }
        search_response = requests.get(SEARCH_SERVICE_URL, params=search_payload).json()
        hotel_ids = search_response['hotelIds']
        if not hotel_ids:
            logging.info("No hotels found for the given location and dates.")
            return jsonify([])

        # Call the profile service
        profile_payload = {
            "hotelIds": hotel_ids
        }
        profile_response = requests.get(PROFILE_SERVICE_URL, params=profile_payload).json()

        # Convert the REST API response to a desired JSON format
        hotels = [{
            'type': 'Feature', 'id': hotel['id'],
            'properties': {'name': hotel['name'], 'phone_number': hotel['phoneNumber']},
            'geometry': {'type': 'Point', 'coordinates': [hotel['address']['lat'], hotel['address']['lon']]}} for hotel
            in profile_response]

        return jsonify(hotels)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'Internal server error'}), 500
