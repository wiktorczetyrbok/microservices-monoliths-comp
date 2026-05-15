// gateway/index.js
import cluster from "cluster";
import express from "express";
import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

const PORT = Number(process.env.PORT ?? 8080);
const WORKERS = Number(process.env.WEB_CONCURRENCY ?? 4);

const SEARCH_SERVICE = process.env.SEARCH_SERVICE ?? "search:8080";
const METADATA_SERVICE = process.env.METADATA_SERVICE ?? "metadata:8080";

if (cluster.isPrimary) {
    console.log(`Primary process ${process.pid} running`);
    console.log(`Starting ${WORKERS} gateway workers`);

    for (let i = 0; i < WORKERS; i++) {
        cluster.fork();
    }

    cluster.on("exit", (worker) => {
        console.log(`Worker ${worker.process.pid} died. Restarting...`);
        cluster.fork();
    });
} else {
    const app = express();

    function loadProto(path) {
        return grpc.loadPackageDefinition(
            protoLoader.loadSync(path, { keepCase: true })
        );
    }

    const searchProto = loadProto("proto/search.proto").search;
    const metadataProto = loadProto("proto/metadata.proto").metadata;

    const searchClient = new searchProto.Search(
        SEARCH_SERVICE,
        grpc.credentials.createInsecure()
    );

    const metadataClient = new metadataProto.Metadata(
        METADATA_SERVICE,
        grpc.credentials.createInsecure()
    );

    app.get("/images/search", (req, res) => {
        try {
            const kernel = Number(req.query.kernel ?? 3);
            const threshold = Number(req.query.threshold ?? 0.9);

            searchClient.Search(
                { kernel, threshold },
                (err, searchRes) => {
                    if (err) {
                        console.error(err);
                        return res.status(503).json({ error: "Search unavailable" });
                    }

                    if (!searchRes.imageIds.length) {
                        return res.json([]);
                    }

                    metadataClient.Get(
                        { imageIds: searchRes.imageIds },
                        (err, metaRes) => {
                            if (err) {
                                console.error(err);
                                return res.status(503).json({ error: "Metadata unavailable" });
                            }

                            return res.json(metaRes.images);
                        }
                    );
                }
            );
        } catch (e) {
            console.error(e);
            return res.status(500).json({ error: "Internal Server Error" });
        }
    });

    app.listen(PORT, "0.0.0.0", () =>
        console.log(`Gateway worker ${process.pid} listening on 0.0.0.0:${PORT}`)
    );
}