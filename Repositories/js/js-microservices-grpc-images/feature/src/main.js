// feature/index.js
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';
import { loadData, imageBuffers } from './data.js';
import { extractFeatures } from './features.js';

const PORT = '0.0.0.0:8080';

const proto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/feature.proto')
).feature;

function Extract(call, callback) {
    const { imageId, kernel } = call.request;
    const buffer = imageBuffers[imageId];

    if (!buffer) {
        return callback(null, { vector: [] });
    }

    const vector = extractFeatures(buffer, kernel);
    callback(null, { vector });
}

loadData();

const server = new grpc.Server();
server.addService(proto.Feature.service, { Extract });
server.bindAsync(PORT, grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('Feature service running on 8080');
});
