package pb.java.microservices.rest.geo.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;
import pb.java.microservices.rest.geo.entity.GeoPoint;

import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class GeoService {
    private static final double MAX_SEARCH_RADIUS = 10;
    private static final int MAX_SEARCH_RESULTS = Integer.MAX_VALUE;
    private static final double EARTH_RADIUS = 6371;
    private static final double RADIANS_CONST = Math.PI / 180;

    private final Map<String, GeoPoint> geoIndex = new HashMap<>();

    private final ResourceLoader resourceLoader;
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Autowired
    public GeoService(ResourceLoader resourceLoader) throws IOException {
        this.resourceLoader = resourceLoader;
        String jsonData = readJsonFile("data/geo.json");

        List<GeoPoint> geoPoints = objectMapper.readValue(jsonData, new TypeReference<List<GeoPoint>>() {});
        for (GeoPoint geoPoint : geoPoints) {
            geoIndex.put(geoPoint.getHotelId(), geoPoint);
        }
    }

    public List<String> getNearbyHotels(float lat, float lon) {
        GeoPoint center = new GeoPoint();
        center.setLat(lat);
        center.setLon(lon);

        return geoIndex.values().stream()
                .map(p -> new AbstractMap.SimpleEntry<>(p, haversineDistance(p, center)))
                .filter(entry -> entry.getValue() <= MAX_SEARCH_RADIUS)
                .sorted(Comparator.comparingDouble(Map.Entry::getValue))
                .map(entry -> entry.getKey().getHotelId())
                .collect(Collectors.toList());
    }

    private String readJsonFile(String filename) throws IOException {
        Resource resource = resourceLoader.getResource("classpath:" + filename);
        InputStreamReader reader = new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8);
        return org.apache.commons.io.IOUtils.toString(reader);
    }

    private double haversineDistance(GeoPoint p1, GeoPoint p2) {
        double latDistance = Math.toRadians(p2.getLat() - p1.getLat());
        double lonDistance = Math.toRadians(p2.getLon() - p1.getLon());

        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
                + Math.cos(Math.toRadians(p1.getLat())) * Math.cos(Math.toRadians(p2.getLat()))
                * Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);

        double centralAngle = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        return EARTH_RADIUS * centralAngle;
    }
}
