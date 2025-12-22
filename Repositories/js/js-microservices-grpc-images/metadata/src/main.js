// metadata/index.js
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';
import { loadData, metadataIndex } from './data.js';

const PORT = '0.0.0.0:8080';

const proto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/metadata.proto')
).metadata;

function Get(call, callback) {
    const images = call.request.imageIds
        .map(id => metadataIndex[id])
        .filter(Boolean);

    callback(null, { images });
}

loadData();

const server = new grpc.Server();
server.addService(proto.Metadata.service, { Get });
server.bindAsync(PORT, grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('Metadata service running on 8080');
});
