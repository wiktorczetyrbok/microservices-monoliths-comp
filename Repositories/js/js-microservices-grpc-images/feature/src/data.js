// feature/data.js
import fs from 'fs';
import path from 'path';

const dataDir = path.join(process.cwd(), 'data');
const imageDir = path.join(dataDir, 'images');

export const imageBuffers = {};



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
    console.log(`[FEATURE] Loaded ${Object.keys(imageBuffers).length} images`);
}
