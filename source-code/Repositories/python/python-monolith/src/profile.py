from src.data_load_module import hotel_profiles_index


def get_hotel_profiles(hotel_ids):
    matching_profiles = [
        hotel_profiles_index.get(hotel_id)
        for hotel_id in hotel_ids
        if hotel_id in hotel_profiles_index
    ]
    if not matching_profiles:
        return []

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
