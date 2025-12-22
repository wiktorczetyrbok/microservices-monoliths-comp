import fs from "fs";
import path from "path";

const dataDir = path.join(process.cwd(), "data");

export const featureIndex = {};

function loadJson(file) {
    return JSON.parse(
        fs.readFileSync(path.join(dataDir, file), "utf-8")
    );
}

export async function loadData() {

    const features = loadJson("features.json");
    features.forEach(f => {
        featureIndex[f.id] = f.vector;
    });



}