import { featureIndex } from "./dataLoadModule.js";

function euclidean(a, b) {
    let sum = 0;
    for (let i = 0; i < a.length; i++) {
        const d = a[i] - b[i];
        sum += d * d;
    }
    return Math.sqrt(sum);
}

export function findSimilarImages(queryVector, threshold) {

    return Object.entries(featureIndex)
        .filter(([id, ref]) => {
            const distance = euclidean(queryVector, ref);

            console.log(`[SIM] ${id} dist=${distance.toFixed(4)}`);

            return distance <= threshold;
        })
        .map(([id]) => id);
}

