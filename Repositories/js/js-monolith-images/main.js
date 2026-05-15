import cluster from "cluster";
import os from "os";
import express from "express";
import { loadData, imageBuffers } from "./dataLoadModule.js";
import { extractFeatures } from "./features.js";
import { findSimilarImages } from "./similarity.js";
import { getImageMetadata } from "./metadata.js";

const PORT = Number(process.env.PORT ?? 8080);
const WORKERS = Number(process.env.WEB_CONCURRENCY ?? 4);

if (cluster.isPrimary) {
    console.log(`Primary process ${process.pid} running`);
    console.log(`Starting ${WORKERS} workers`);

    for (let i = 0; i < WORKERS; i++) {
        cluster.fork();
    }

    cluster.on("exit", (worker) => {
        console.log(`Worker ${worker.process.pid} died. Restarting...`);
        cluster.fork();
    });
} else {
    const app = express();

    await loadData();

    const firstImageId = Object.keys(imageBuffers)[0];
    const queryImage = imageBuffers[firstImageId];

    const queryVectorCache = new Map();

    app.get("/images/search", (req, res) => {
        try {
            const threshold = Number(req.query.threshold ?? 0.2);
            const kernel = Number(req.query.kernel ?? 3);

            let queryVector = queryVectorCache.get(kernel);

            if (!queryVector) {
                queryVector = extractFeatures(queryImage, kernel);
                queryVectorCache.set(kernel, queryVector);
            }

            const matches = findSimilarImages(queryVector, threshold);

            if (!matches.length) {
                return res.json([]);
            }

            const metadata = getImageMetadata(matches);
            return res.json(metadata);
        } catch (e) {
            console.error(e);
            return res.status(500).json({ error: "Internal Server Error" });
        }
    });

    app.listen(PORT, () =>
        console.log(`Worker ${process.pid} listening on port ${PORT}`)
    );
}