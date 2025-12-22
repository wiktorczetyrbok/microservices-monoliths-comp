// metadata/data.js
import fs from 'fs';
import path from 'path';

const dataDir = path.join(process.cwd(), 'data');

export const metadataIndex = {};

function loadJson(file) {
    return JSON.parse(
        fs.readFileSync(path.join(dataDir, file), 'utf-8')
    );
}

export function loadData() {
    const metadata = loadJson('metadata.json');

    metadata.forEach(m => {
        metadataIndex[m.id] = m;
    });

    console.log(
        `[METADATA] Loaded ${Object.keys(metadataIndex).length} records`
    );
}
