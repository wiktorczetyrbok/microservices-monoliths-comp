import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// data_store = {}
export const dataStore = {};

// hotel_profiles_index = {}
export const hotelProfilesIndex = {};

// def load_data():
export function loadData() {
    const dataFile = 'hotels.json';
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

// def build_hotel_profiles_index():
export function buildHotelProfilesIndex() {
    const hotels = dataStore['hotels.json'] || [];

    for (const hotel of hotels) {
        const hotelId = hotel.id;
        hotelProfilesIndex[hotelId] = hotel;
    }
}
