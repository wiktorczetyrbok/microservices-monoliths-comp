package pb.java.microservices.monolith.App.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;
import org.springframework.util.FileCopyUtils;
import pb.java.microservices.monolith.App.entity.Hotel;

import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Function;
import java.util.logging.Logger;
import java.util.stream.Collectors;

@Service
public class ProfileService {
    private static final Logger LOGGER = Logger.getLogger(ProfileService.class.getName());
    private final ResourceLoader resourceLoader;
    private Map<String, Hotel> profiles = new ConcurrentHashMap<>();

    public ProfileService(ResourceLoader resourceLoader) {
        this.resourceLoader = resourceLoader;
    }

    @PostConstruct
    public void init() {
        try {
            loadProfilesFromJsonFile("data/hotels.json");
            LOGGER.info("Profiles loaded successfully");
        } catch (IOException e) {
            LOGGER.severe("Failed to load profiles: " + e.getMessage());
        }
    }

    public Hotel getProfileById(String id) {
        Hotel hotel = profiles.get(id);
        if (hotel == null) {
            LOGGER.warning("No profile found for id: " + id);
        }
        return hotel;
    }

    public List<Hotel> getProfiles(List<String> ids) {
        // Ensuring that only non-null profiles are returned in the list
        return ids.stream().map(profiles::get).filter(Objects::nonNull).collect(Collectors.toList());
    }

    private void loadProfilesFromJsonFile(String filename) throws IOException {
        String jsonData = readJsonFile(filename);
        List<Hotel> hotelList = parseJsonToHotelList(jsonData);
        this.profiles = hotelList.stream().collect(Collectors.toMap(Hotel::getId, Function.identity()));
    }

    private List<Hotel> parseJsonToHotelList(String jsonData) throws IOException {
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.readValue(jsonData, new TypeReference<List<Hotel>>() {
        });
    }

    private String readJsonFile(String filename) throws IOException {
        Resource resource = resourceLoader.getResource("classpath:" + filename);
        try (InputStreamReader reader = new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8)) {
            return FileCopyUtils.copyToString(reader);
        }
    }
}
