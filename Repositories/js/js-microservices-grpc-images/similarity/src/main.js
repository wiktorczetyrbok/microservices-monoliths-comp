// similarity/index.js
import cluster from "cluster";
import os from "os";
import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";
import { loadData, featureIndex } from "./data.js";

const PORT = process.env.PORT ?? "8080";
const ADDRESS = `0.0.0.0:${PORT}`;
const WORKERS = Number(process.env.WEB_CONCURRENCY ?? 4);

if (cluster.isPrimary) {
    console.log(`Primary process ${process.pid} running`);
    console.log(`Starting ${WORKERS} similarity workers`);

    for (let i = 0; i < WORKERS; i++) {
        cluster.fork();
    }

    cluster.on("exit", (worker) => {
        console.log(`Worker ${worker.process.pid} died. Restarting...`);
        cluster.fork();
    });
} else {
    const proto = grpc.loadPackageDefinition(
        protoLoader.loadSync("proto/similarity.proto")
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
        try {
            const { queryVector, threshold } = call.request;

            const imageIds = Object.entries(featureIndex)
                .filter(([id, ref]) => {
                    const dist = euclidean(queryVector, ref);
                    console.log(`[SIM] ${id} dist=${dist.toFixed(4)}`);
                    return dist <= threshold;
                })
                .map(([id]) => id);

            callback(null, { imageIds });
        } catch (e) {
            console.error(e);
            callback(e);
        }
    }

    loadData();

    const server = new grpc.Server();

    server.addService(proto.Similarity.service, { Find });

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
                `Similarity worker ${process.pid} running on 0.0.0.0:${port}`
            );
        }
    );
}