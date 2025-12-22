import { metadataIndex } from "./dataLoadModule.js";

export function getImageMetadata(ids) {
    return ids
        .map(id => metadataIndex[id])
        .filter(Boolean)
        .map(m => ({
            id: m.id,
            name: m.name,
            tags: m.tags
        }));
}
