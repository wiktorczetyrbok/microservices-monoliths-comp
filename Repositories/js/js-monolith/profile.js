import { hotelProfilesIndex } from "./dataLoadModule.js";

export function getHotelProfiles(hotelIds) {
    return hotelIds
        .map(id => hotelProfilesIndex[id])
        .filter(Boolean)
        .map(hotel => ({
            id: hotel.id,
            name: hotel.name,
            phoneNumber: hotel.phoneNumber,
            description: hotel.description,
            address: hotel.address
        }));
}