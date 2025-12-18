import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';
import {
    loadData,
    buildHotelProfilesIndex,
    hotelProfilesIndex
} from './data.js';

const PORT = '0.0.0.0:8080';

const proto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/profile.proto')
).profile;

function GetProfiles(call, callback) {
    const hotels = call.request.hotelIds
        .map(id => hotelProfilesIndex[id])
        .filter(Boolean);

    callback(null, { hotels });
}

loadData();
buildHotelProfilesIndex();

const server = new grpc.Server();
server.addService(proto.Profile.service, { GetProfiles });
server.bindAsync(PORT, grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('Profile service running on 8080');
});
