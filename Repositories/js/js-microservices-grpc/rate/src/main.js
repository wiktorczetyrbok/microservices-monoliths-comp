import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';
import { loadData, buildInventoryIndex, inventoryIndex } from './data.js';

const PORT = '0.0.0.0:8080';

const proto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/rate.proto')
).rate;

function GetRates(call, callback) {
    const { hotelIds, inDate, outDate } = call.request;
    const ratePlans = [];

    for (const id of hotelIds) {
        const rate = inventoryIndex?.[id]?.[inDate]?.[outDate];
        if (rate) ratePlans.push({ hotelId: id, ...rate });
    }

    callback(null, { ratePlans });
}

loadData();
buildInventoryIndex();

const server = new grpc.Server();
server.addService(proto.Rate.service, { GetRates });
server.bindAsync(PORT, grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('Rate service running on 8080');
});
