package pb.java.microservices.rest.gateway.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import pb.java.microservices.rest.gateway.entity.Hotel;

import java.util.*;

@Service
public class GatewayService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${search.service.path}")
    private String searchServicePath;

    @Value("${profile.service.path}")
    private String profileServicePath;

    public Map<String, Object> searchHotels(String inDate, String outDate, float lat, float lon) {

        // Making REST call for search service
        Map<String, Object> searchParams = new HashMap<>();
        searchParams.put("inDate", inDate);
        searchParams.put("outDate", outDate);
        searchParams.put("lat", lat);
        searchParams.put("lon", lon);

        ResponseEntity<List<String>> searchResponse = restTemplate.exchange(
                searchServicePath,
                HttpMethod.POST,
                new HttpEntity<>(searchParams),
                new ParameterizedTypeReference<List<String>>() {}
        );
        List<String> hotelIds = searchResponse.getBody();

        // Making REST call for profile service
        ResponseEntity<List<Hotel>> profileResponse = restTemplate.exchange(
                profileServicePath,
                HttpMethod.POST,
                new HttpEntity<>(hotelIds),
                new ParameterizedTypeReference<List<Hotel>>() {}
        );
        List<Hotel> hotels = profileResponse.getBody();

        return geoJSONResponse(hotels);
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
