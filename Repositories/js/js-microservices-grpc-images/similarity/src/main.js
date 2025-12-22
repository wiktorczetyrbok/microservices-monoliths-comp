// similarity/index.js
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';
import { loadData, featureIndex } from './data.js';

const PORT = '0.0.0.0:8080';

const proto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/similarity.proto')
).similarity;

function euclidean(a, b) {
    let sum = 0;
    for (let i = 0; i < a.length; i++) {
        const d = a[i] - b[i];
        sum += d * d;
    }
    return Math.sqrt(sum);
}

function Find(call, callback) {
    const { queryVector, threshold } = call.request;

    const imageIds = Object.entries(featureIndex)
        .filter(([id, ref]) => {
            const dist = euclidean(queryVector, ref);
            console.log(`[SIM] ${id} dist=${dist.toFixed(4)}`);
            return dist <= threshold;
        })
        .map(([id]) => id);

    callback(null, { imageIds });
}

loadData();

const server = new grpc.Server();
server.addService(proto.Similarity.service, { Find });
server.bindAsync(PORT, grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('Similarity service running on 8080');
});
