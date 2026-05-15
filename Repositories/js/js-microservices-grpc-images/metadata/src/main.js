// metadata/index.js
import cluster from "cluster";
import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";
import { loadData, metadataIndex } from "./data.js";

const PORT = process.env.PORT ?? "8080";
const ADDRESS = `0.0.0.0:${PORT}`;
const WORKERS = Number(process.env.WEB_CONCURRENCY ?? 4);

if (cluster.isPrimary) {
    console.log(`Primary process ${process.pid} running`);
    console.log(`Starting ${WORKERS} metadata workers`);

    for (let i = 0; i < WORKERS; i++) {
        cluster.fork();
    }

    cluster.on("exit", (worker) => {
        console.log(`Worker ${worker.process.pid} died. Restarting...`);
        cluster.fork();
    });
} else {
    const proto = grpc.loadPackageDefinition(
        protoLoader.loadSync("proto/metadata.proto")
    ).metadata;

    function Get(call, callback) {
        try {
            const images = call.request.imageIds
                .map((id) => metadataIndex[id])
                .filter(Boolean);

            callback(null, { images });
        } catch (e) {
            console.error(e);
            callback(e);
        }
    }

    loadData();

    const server = new grpc.Server();

    server.addService(proto.Metadata.service, { Get });

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
                `Metadata worker ${process.pid} running on 0.0.0.0:${port}`
            );
        }
    );
}