import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// === Python equivalents ===
// current_dir = os.path.dirname(os.path.abspath(__file__))
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// data_store = {}
export const dataStore = {};

// hotel_geo_data = {}
export const hotelGeoData = {};

// def load_data():
export function loadData() {
    const dataFile = 'geo.json';
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

// def build_hotel_geo_data():
export function buildHotelGeoData() {
    const hotels = dataStore['geo.json'] || [];

    for (const item of hotels) {
        const hotelId = item.hotelId;
        hotelGeoData[hotelId] = {
            lat: item.lat,
            lon: item.lon,
            data: item
        };
    }
}
