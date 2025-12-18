import { inventoryIndex } from "./dataLoadModule.js";

export function getRates(hotelIds, inDate, outDate) {
    const ratePlans = [];

    hotelIds.forEach(id => {
        const rate =
            inventoryIndex[id]?.[inDate]?.[outDate];

        if (rate) {
            ratePlans.push({
                hotelId: id,
                code: rate.code,
                inDate,
                outDate,
                roomType: rate.roomType
            });
        }
    });

    return { ratePlans };
}