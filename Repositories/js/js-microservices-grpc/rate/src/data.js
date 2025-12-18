import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// data_store = {}
export const dataStore = {};

// inventory_index = defaultdict(lambda: defaultdict(dict))
export const inventoryIndex = {};

// def load_data():
export function loadData() {
    const dataFile = 'inventory.json';
    const jsonFile = path.join(__dirname, '..', 'data', dataFile);

    try {
        const raw = fs.readFileSync(jsonFile, 'utf-8');
        dataStore[dataFile] = JSON.parse(raw);
    } catch (err) {
        if (err.code === 'ENOENT') {
            console.error(`Error: File ${dataFile} not found in ${jsonFile}`);
        } else if (err instanceof SyntaxError) {
            console.error(`Error: File ${dataFile} is not a valid JSON file`);
        } else {
            throw err;
        }
    }
}

// def build_inventory_index():
export function buildInventoryIndex() {
    const inventoryData = dataStore['inventory.json'] || [];

    for (const item of inventoryData) {
        const { hotelId, inDate, outDate } = item;

        inventoryIndex[hotelId] ??= {};
        inventoryIndex[hotelId][inDate] ??= {};
        inventoryIndex[hotelId][inDate][outDate] = item;
    }
}
