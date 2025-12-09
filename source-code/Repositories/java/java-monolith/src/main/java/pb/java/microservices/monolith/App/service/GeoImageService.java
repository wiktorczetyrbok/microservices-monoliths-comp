package pb.java.microservices.monolith.App.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;
import pb.java.microservices.monolith.App.entity.ImageMeta;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class GeoImageService {
    private final Map<String, ImageMeta> imageMetaMap = new HashMap<>();
    private final ResourceLoader resourceLoader;
    private static final double MAX_RADIUS_KM = 5.0;
    private static final double EARTH_RADIUS = 6371.0;

    public GeoImageService(ResourceLoader resourceLoader) {
        this.resourceLoader = resourceLoader;
    }

    @PostConstruct
    public void init() {
        try {
            Resource resource = resourceLoader.getResource("classpath:data/images.json");
            InputStreamReader reader = new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8);
            ObjectMapper mapper = new ObjectMapper();
            List<ImageMeta> images = mapper.readValue(reader, new TypeReference<>() {});
            for (ImageMeta image : images) {
                imageMetaMap.put(image.getId(), image);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public List<String> getNearbyImageIds(float lat, float lon) {
        return imageMetaMap.values().stream()
                .filter(image -> haversine(lat, lon, image.getLat(), image.getLon()) <= MAX_RADIUS_KM)
                .map(ImageMeta::getId)
                .collect(Collectors.toList());
    }

    private double haversine(double lat1, double lon1, double lat2, double lon2) {
        double dLat = Math.toRadians(lat2 - lat1);
        double dLon = Math.toRadians(lon2 - lon1);
        double a = Math.pow(Math.sin(dLat / 2), 2)
                + Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2))
                * Math.pow(Math.sin(dLon / 2), 2);
        return EARTH_RADIUS * 2 * Math.asin(Math.sqrt(a));
    }
}
