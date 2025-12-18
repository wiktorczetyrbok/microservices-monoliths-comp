import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';

const PORT = '0.0.0.0:8080';
const GEO_SERVICE_ADDRESS = 'geo:8080';
const RATE_SERVICE_ADDRESS = 'rate:8080';

const geoProto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/geo.proto')
).geo;

const rateProto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/rate.proto')
).rate;

const searchProto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/search.proto')
).search;

const geoClient = new geoProto.Geo(
    GEO_SERVICE_ADDRESS,
    grpc.credentials.createInsecure()
);

const rateClient = new rateProto.Rate(
    RATE_SERVICE_ADDRESS,
    grpc.credentials.createInsecure()
);
function Nearby(call, callback) {
    geoClient.Nearby(
        { lat: call.request.lat, lon: call.request.lon },
        (geoErr, geoRes) => {
            if (geoErr) return callback(geoErr);

            rateClient.GetRates(
                {
                    hotelIds: geoRes.hotelIds ?? [],
                    inDate: call.request.inDate,
                    outDate: call.request.outDate
                },
                (rateErr, rateRes) => {
                    if (rateErr) return callback(rateErr);

                    const ratePlans = rateRes?.ratePlans ?? [];

                    callback(null, {
                        hotelIds: ratePlans.map(r => r.hotelId)
                    });
                }
            );
        }
    );
}


const server = new grpc.Server();
server.addService(searchProto.Search.service, { Nearby });
server.bindAsync(PORT, grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('Search service running on 8080');
});
