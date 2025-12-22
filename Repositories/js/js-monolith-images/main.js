import express from "express";
import { loadData, imageBuffers } from "./dataLoadModule.js";
import { extractFeatures } from "./features.js";
import { findSimilarImages } from "./similarity.js";
import { getImageMetadata } from "./metadata.js";

const app = express();

await loadData();

app.get("/images/search", (req, res) => {
    try {
        const threshold = Number(req.query.threshold ?? 0.2);
        const kernel = Number(req.query.kernel ?? 3);

        // Fixed query image (like geo center point)
        const firstImageId = Object.keys(imageBuffers)[0];
        const queryImage = imageBuffers[firstImageId];

        const queryVector = extractFeatures(queryImage, kernel);

        const matches = findSimilarImages(
            queryVector,
            threshold
        );

        if (!matches.length) return res.json([]);

        const metadata = getImageMetadata(matches);
        res.json(metadata);
    } catch (e) {
        console.error(e);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

app.listen(8080, () =>
    console.log("Image monolith running on http://localhost:8080")
);
