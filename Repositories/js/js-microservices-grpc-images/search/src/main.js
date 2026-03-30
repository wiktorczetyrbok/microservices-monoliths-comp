// search/index.js
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';

const PORT = '0.0.0.0:8080';
const FEATURE_SERVICE = 'feature:8080';
const SIMILARITY_SERVICE = 'similarity:8080';

const featureProto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/feature.proto')
).feature;

const similarityProto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/similarity.proto')
).similarity;

const searchProto = grpc.loadPackageDefinition(
    protoLoader.loadSync('proto/search.proto')
).search;

const featureClient = new featureProto.Feature(
    FEATURE_SERVICE,
    grpc.credentials.createInsecure()
);

const similarityClient = new similarityProto.Similarity(
    SIMILARITY_SERVICE,
    grpc.credentials.createInsecure()
);

function Search(call, callback) {
    const { kernel, threshold } = call.request;

    // fixed reference image
    featureClient.Extract(
        { imageId: 'img001', kernel },
        (err, featureRes) => {
            if (err) return callback(err);

            similarityClient.Find(
                {
                    queryVector: featureRes.vector,
                    threshold
                },
                (err, simRes) => {
                    if (err) return callback(err);
                    callback(null, { imageIds: simRes.imageIds });
                }
            );
        }
    );
}

const server = new grpc.Server();
server.addService(searchProto.Search.service, { Search });
server.bindAsync(PORT, grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('Search service running on 8080');
});
