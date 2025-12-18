import express from 'express';
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';

const app = express();
const PORT = 8080;

const SEARCH_SERVICE_ADDRESS = 'search:8080';
const PROFILE_SERVICE_ADDRESS = 'profile:8080';

function loadProto(path) {
    return grpc.loadPackageDefinition(
        protoLoader.loadSync(path, { keepCase: true })
    );
}

const searchProto = loadProto('proto/search.proto').search;
const profileProto = loadProto('proto/profile.proto').profile;

const searchClient = new searchProto.Search(
    SEARCH_SERVICE_ADDRESS,
    grpc.credentials.createInsecure()
);

const profileClient = new profileProto.Profile(
    PROFILE_SERVICE_ADDRESS,
    grpc.credentials.createInsecure()
);

app.get('/hotels', (req, res) => {
    const { inDate, outDate, lat = 0, lon = 0 } = req.query;

    if (!inDate || !outDate) {
        return res.status(400).json({ error: 'Invalid date parameters' });
    }

    searchClient.Nearby(
        {
            lat: parseFloat(lat),
            lon: parseFloat(lon),
            inDate,
            outDate
        },
        (err, searchResp) => {
            if (err) {
                return res.status(503).json({ error: 'Search unavailable' });
            }

            const hotelIds = searchResp?.hotelIds ?? [];

            if (hotelIds.length === 0) {
                return res.json([]);
            }

            profileClient.GetProfiles(
                { hotelIds },
                (err, profileResp) => {
                    if (err) {
                        return res.status(503).json({ error: 'Profile unavailable' });
                    }

                    const hotels = (profileResp.hotels ?? []).map(hotel => ({
                        type: 'Feature',
                        id: hotel.id,
                        properties: {
                            name: hotel.name,
                            phone_number: hotel.phoneNumber
                        },
                        geometry: {
                            type: 'Point',
                            coordinates: [hotel.address.lat, hotel.address.lon]
                        }
                    }));

                    res.json(hotels);
                }
            );
        }
    );
});

app.listen(PORT, '0.0.0.0', () =>
    console.log(`Gateway listening on 0.0.0.0:${PORT}`)
);
