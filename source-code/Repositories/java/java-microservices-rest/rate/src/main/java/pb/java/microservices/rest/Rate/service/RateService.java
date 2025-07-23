package pb.java.microservices.rest.Rate.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;
import org.springframework.util.FileCopyUtils;
import pb.java.microservices.rest.Rate.entity.RatePlan;
import pb.java.microservices.rest.Rate.entity.Stay;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
public class RateService {
    private Map<Stay, RatePlan> rateTable = new HashMap<>();
    private final ResourceLoader resourceLoader;

    @Autowired
    public RateService(ResourceLoader resourceLoader) throws IOException {
        this.resourceLoader = resourceLoader;
        loadRateTableFromJsonFile("data/inventory.json");
    }

    public List<RatePlan> getRates(List<String> hotelIds, String inDate, String outDate) {
        List<RatePlan> results = new ArrayList<>();
        for (String hotelId : hotelIds) {
            Stay stay = new Stay(hotelId, inDate, outDate);
            RatePlan ratePlan = rateTable.get(stay);
            if (ratePlan != null) {
                results.add(ratePlan);
            }
        }
        return results;
    }

    private void loadRateTableFromJsonFile(String filename) throws IOException {
        Resource resource = resourceLoader.getResource("classpath:" + filename);
        ObjectMapper mapper = new ObjectMapper();
        mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        try (InputStream is = resource.getInputStream()) {
            List<RatePlan> ratePlans = mapper.readValue(is, new TypeReference<List<RatePlan>>() {});
            for (RatePlan ratePlan : ratePlans) {
                Stay stay = new Stay(ratePlan.getHotelId(), ratePlan.getInDate(), ratePlan.getOutDate());
                this.rateTable.put(stay, ratePlan);
            }
        } catch (Exception e) {
            e.printStackTrace(); // Important for debugging
        }
    }
}
