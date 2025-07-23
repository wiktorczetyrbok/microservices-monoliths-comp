package pb.java.microservices.rest.profile.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;
import org.springframework.util.FileCopyUtils;
import pb.java.microservices.rest.profile.entity.Hotel;

import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
public class ProfileService {

    private Map<String, Hotel> profiles;
    private final ResourceLoader resourceLoader;

    public ProfileService(ResourceLoader resourceLoader) throws IOException {
        this.resourceLoader = resourceLoader;
        loadProfilesFromJsonFile("data/hotels.json");
    }

    public Hotel getProfileById(String id) {
        return profiles.get(id);
    }

    public List<Hotel> getProfiles(List<String> ids) {
        return ids.stream().map(profiles::get).collect(Collectors.toList());
    }

    private void loadProfilesFromJsonFile(String filename) throws IOException {
        String jsonData = readJsonFile(filename);
        List<Hotel> hotelList = parseJsonToHotelList(jsonData);
        this.profiles = hotelList.stream().collect(Collectors.toMap(Hotel::getId, Function.identity()));
    }

    private List<Hotel> parseJsonToHotelList(String jsonData) throws IOException {
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.readValue(jsonData, new TypeReference<List<Hotel>>() {});
    }

    private String readJsonFile(String filename) throws IOException {
        Resource resource = resourceLoader.getResource("classpath:" + filename);
        InputStreamReader reader = new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8);
        return FileCopyUtils.copyToString(reader);
    }
}
