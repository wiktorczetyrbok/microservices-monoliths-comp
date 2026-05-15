// feature/index.js
import cluster from "cluster";
import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";
import { loadData, imageBuffers } from "./data.js";
import { extractFeatures } from "./features.js";

const PORT = process.env.PORT ?? "8080";
const ADDRESS = `0.0.0.0:${PORT}`;
const WORKERS = Number(process.env.WEB_CONCURRENCY ?? 4);

if (cluster.isPrimary) {
    console.log(`Primary process ${process.pid} running`);
    console.log(`Starting ${WORKERS} feature workers`);

    for (let i = 0; i < WORKERS; i++) {
        cluster.fork();
    }

    cluster.on("exit", (worker) => {
        console.log(`Worker ${worker.process.pid} died. Restarting...`);
        cluster.fork();
    });
} else {
    const proto = grpc.loadPackageDefinition(
        protoLoader.loadSync("proto/feature.proto")
    ).feature;

    const featureCache = new Map();

    function Extract(call, callback) {
        try {
            const { imageId, kernel } = call.request;
            const buffer = imageBuffers[imageId];

            if (!buffer) {
                return callback(null, { vector: [] });
            }

            const cacheKey = `${imageId}:${kernel}`;

            let vector = featureCache.get(cacheKey);

            if (!vector) {
                vector = extractFeatures(buffer, kernel);
                featureCache.set(cacheKey, vector);
            }

            return callback(null, { vector });
        } catch (e) {
            console.error(e);
            return callback(e);
        }
    }

    loadData();

    const server = new grpc.Server();

    server.addService(proto.Feature.service, { Extract });

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
                `Feature worker ${process.pid} running on 0.0.0.0:${port}`
            );
        }
    );
}