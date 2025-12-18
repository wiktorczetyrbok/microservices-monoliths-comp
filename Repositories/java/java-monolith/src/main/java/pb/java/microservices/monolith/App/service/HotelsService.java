package pb.java.microservices.monolith.App.service;

import org.springframework.stereotype.Service;
import pb.java.microservices.monolith.App.entity.Hotel;
import pb.java.microservices.monolith.App.entity.RatePlan;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class HotelsService {

    private final ProfileService profileService;
    private final GeoService geoService;
    private final RateService rateService;

    public HotelsService(ProfileService profileService, GeoService geoService, RateService rateService) {
        this.profileService = profileService;
        this.geoService = geoService;
        this.rateService = rateService;
    }
    public Map<String, Object> searchHotels(String inDate, String outDate, float lat, float lon) {
        List<String> searchServiceResponse = searchServiceFunctionality(inDate, outDate, lat, lon);
        List<Hotel> profileServiceResponse = profileServiceFunctionality(searchServiceResponse);
        return geoJSONResponse(profileServiceResponse);
    }

    public List<String> searchServiceFunctionality(String inDate, String outDate, float lat, float lon) {
        List<String> geoHotelIds = geoServiceFunctionality(lat, lon);
        List<RatePlan> rateServiceResponse = rateServiceFunctionality(geoHotelIds, inDate, outDate);

        return rateServiceResponse.stream()
                .map(RatePlan::getHotelId)
                .collect(Collectors.toList());
    }

    public List<Hotel> profileServiceFunctionality(List<String> hotelIds) {
        return profileService.getProfiles(hotelIds);
    }

    public List<String> geoServiceFunctionality(float lat, float lon) {
        return geoService.getNearbyHotels(lat, lon);
    }

    public List<RatePlan> rateServiceFunctionality(List<String> hotelIds, String indate, String outdate) {
        return rateService.getRates(hotelIds, indate, outdate);
    }

    private Map<String, Object> geoJSONResponse(List<Hotel> hotels) {
        List<Map<String, Object>> features = new ArrayList<>();
        for (Hotel hotel : hotels) {
            Map<String, Object> feature = new HashMap<>();
            feature.put("type", "Feature");
            feature.put("id", hotel.getId());

            Map<String, String> properties = new HashMap<>();
            properties.put("name", hotel.getName());
            properties.put("phone_number", hotel.getPhoneNumber());

            Map<String, Object> geometry = new HashMap<>();
            geometry.put("type", "Point");
            List<Float> coordinates = Arrays.asList(hotel.getAddress().getLon(), hotel.getAddress().getLat());
            geometry.put("coordinates", coordinates);

            feature.put("properties", properties);
            feature.put("geometry", geometry);

            features.add(feature);
        }

        Map<String, Object> geoJson = new HashMap<>();
        geoJson.put("type", "FeatureCollection");
        geoJson.put("features", features);

        return geoJson;
    }
}
