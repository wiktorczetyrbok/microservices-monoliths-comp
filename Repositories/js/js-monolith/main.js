import express from "express";
import { loadData } from "./dataLoadModule.js";
import { getNearbyHotels } from "./geo.js";
import { getRates } from "./rate.js";
import { getHotelProfiles } from "./profile.js";

const app = express();
loadData();

app.get("/hotels", (req, res) => {
    try {
        const { inDate, outDate, lat, lon } = req.query;

        if (!inDate || !outDate) {
            return res.status(400).json({ error: "Invalid date parameters" });
        }

        const nearbyHotels = getNearbyHotels(Number(lat), Number(lon));
        if (!nearbyHotels.length) return res.json([]);

        const rates = getRates(nearbyHotels, inDate, outDate);
        if (!rates.ratePlans.length) return res.json([]);

        const profileIds = rates.ratePlans.map(r => r.hotelId);
        const profiles = getHotelProfiles(profileIds);

        const response = profiles.map(hotel => ({
            type: "Feature",
            id: hotel.id,
            properties: {
                name: hotel.name,
                phone_number: hotel.phoneNumber
            },
            geometry: {
                type: "Point",
                coordinates: [hotel.address.lat, hotel.address.lon]
            }
        }));

        res.json(response);
    } catch (e) {
        console.error(e);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

app.listen(8080, () =>
    console.log("Node monolith running on http://localhost:8080")
);
