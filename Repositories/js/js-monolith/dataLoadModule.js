import fs from "fs";
import path from "path";

const dataDir = path.join(process.cwd(), "data");

export const hotelGeoData = {};
export const inventoryIndex = {};
export const hotelProfilesIndex = {};

function loadJson(file) {
    return JSON.parse(fs.readFileSync(path.join(dataDir, file)));
}

export function loadData() {
    const geo = loadJson("geo.json");
    const hotels = loadJson("hotels.json");
    const inventory = loadJson("inventory.json");

    // geo
    geo.forEach(item => {
        hotelGeoData[item.hotelId] = {
            lat: item.lat,
            lon: item.lon,
            data: item
        };
    });

    // inventory
    inventory.forEach(item => {
        inventoryIndex[item.hotelId] ??= {};
        inventoryIndex[item.hotelId][item.inDate] ??= {};
        inventoryIndex[item.hotelId][item.inDate][item.outDate] = item;
    });

    // profiles
    hotels.forEach(hotel => {
        hotelProfilesIndex[hotel.id] = hotel;
    });
}