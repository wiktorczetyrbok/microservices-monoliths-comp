package pb.java.microservices.monolith.App.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
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
public class MetaService {

    private final ResourceLoader resourceLoader;
    private final Map<String, ImageMeta> imageMetaMap = new HashMap<>();

    public MetaService(ResourceLoader resourceLoader) {
        this.resourceLoader = resourceLoader;
    }

    @PostConstruct
    public void init() {
        try {
            Resource resource = resourceLoader.getResource("classpath:data/images.json");
            InputStreamReader reader = new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8);

            ObjectMapper mapper = new ObjectMapper();
            mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

            List<ImageMeta> imageList = mapper.readValue(reader, new TypeReference<>() {});
            for (ImageMeta image : imageList) {
                imageMetaMap.put(image.getId(), image);
            }

            System.out.println("Loaded image metadata: " + imageMetaMap.size());

        } catch (Exception e) {
            System.err.println("Failed to load image metadata: " + e.getMessage());
        }
    }

    public List<ImageMeta> getMetadata(List<String> ids) {
        return ids.stream()
                .map(imageMetaMap::get)
                .filter(Objects::nonNull)
                .collect(Collectors.toList());
    }
}
