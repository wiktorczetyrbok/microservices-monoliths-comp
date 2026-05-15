// search/index.js
import cluster from "cluster";
import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

const PORT = process.env.PORT ?? "8080";
const ADDRESS = `0.0.0.0:${PORT}`;
const WORKERS = Number(process.env.WEB_CONCURRENCY ?? 4);

const FEATURE_SERVICE = process.env.FEATURE_SERVICE ?? "feature:8080";
const SIMILARITY_SERVICE = process.env.SIMILARITY_SERVICE ?? "similarity:8080";

if (cluster.isPrimary) {
    console.log(`Primary process ${process.pid} running`);
    console.log(`Starting ${WORKERS} search workers`);

    for (let i = 0; i < WORKERS; i++) {
        cluster.fork();
    }

    cluster.on("exit", (worker) => {
        console.log(`Worker ${worker.process.pid} died. Restarting...`);
        cluster.fork();
    });
} else {
    const featureProto = grpc.loadPackageDefinition(
        protoLoader.loadSync("proto/feature.proto")
    ).feature;

    const similarityProto = grpc.loadPackageDefinition(
        protoLoader.loadSync("proto/similarity.proto")
    ).similarity;

    const searchProto = grpc.loadPackageDefinition(
        protoLoader.loadSync("proto/search.proto")
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
        try {
            const { kernel, threshold } = call.request;

            featureClient.Extract(
                { imageId: "img001", kernel },
                (err, featureRes) => {
                    if (err) {
                        return callback(err);
                    }

                    similarityClient.Find(
                        {
                            queryVector: featureRes.vector,
                            threshold
                        },
                        (err, simRes) => {
                            if (err) {
                                return callback(err);
                            }

                            return callback(null, {
                                imageIds: simRes.imageIds
                            });
                        }
                    );
                }
            );
        } catch (e) {
            console.error(e);
            return callback(e);
        }
    }

    const server = new grpc.Server();

    server.addService(searchProto.Search.service, { Search });

    server.bindAsync(
        ADDRESS,
        grpc.ServerCredentials.createInsecure(),
        (error, port) => {
            if (error) {
                console.error(error);
                process.exit(1);
            }

            server.start();
            console.log(
                `Search worker ${process.pid} running on 0.0.0.0:${port}`
            );
        }
    );
}