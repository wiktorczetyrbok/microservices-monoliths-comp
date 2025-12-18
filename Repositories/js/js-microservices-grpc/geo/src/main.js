import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';
import { loadData, buildHotelGeoData, hotelGeoData } from './data.js';

const PORT = '0.0.0.0:8080';
const EARTH_RADIUS_KM = 6371;
const MAX_RADIUS = 10;

function haversine(a, b) {
    const toRad = x => (x * Math.PI) / 180;
    const dLat = toRad(b.lat - a.lat);
    const dLon = toRad(b.lon - a.lon);

    const h =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(toRad(a.lat)) *
        Math.cos(toRad(b.lat)) *
        Math.sin(dLon / 2) ** 2;

    return 2 * EARTH_RADIUS_KM * Math.asin(Math.sqrt(h));
}

const packageDef = protoLoader.loadSync('proto/geo.proto');
const geoProto = grpc.loadPackageDefinition(packageDef).geo;

function Nearby(call, callback) {
    const point = { lat: call.request.lat, lon: call.request.lon };

    const hotelIds = Object.entries(hotelGeoData)
        .filter(([_, h]) => haversine(point, h) <= MAX_RADIUS)
        .map(([id]) => id);

    callback(null, { hotelIds });
}

loadData();
buildHotelGeoData();

const server = new grpc.Server();
server.addService(geoProto.Geo.service, { Nearby });
server.bindAsync(PORT, grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('Geo service running on 8080');
});
