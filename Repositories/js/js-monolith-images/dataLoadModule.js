import fs from "fs";
import path from "path";

const dataDir = path.join(process.cwd(), "data");
const imageDir = path.join(dataDir, "images");

export const imageBuffers = {};
export const featureIndex = {};
export const metadataIndex = {};

function loadJson(file) {
    return JSON.parse(
        fs.readFileSync(path.join(dataDir, file), "utf-8")
    );
}


function loadImages() {
    const files = fs.readdirSync(imageDir);

    files.forEach(file => {
        const id = path.parse(file).name;
        imageBuffers[id] = fs.readFileSync(
            path.join(imageDir, file)
        );
    });
}

export async function loadData() {

    loadImages();

    const features = loadJson("features.json");
    const metadata = loadJson("metadata.json");

    features.forEach(f => {
        featureIndex[f.id] = f.vector;
    });

    metadata.forEach(m => {
        metadataIndex[m.id] = m;
    });

    console.log(
        `Loaded ${Object.keys(imageBuffers).length} images`
    );
}
