package pb.java.microservices.monolith.App.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;
import pb.java.microservices.monolith.App.entity.ImageJob;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class JobService {

    private final ResourceLoader resourceLoader;
    private final List<ImageJob> jobList = new ArrayList<>();

    public JobService(ResourceLoader resourceLoader) {
        this.resourceLoader = resourceLoader;
    }

    @PostConstruct
    public void init() {
        try {
            Resource resource = resourceLoader.getResource("classpath:data/jobs.json");
            InputStreamReader reader = new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8);

            ObjectMapper mapper = new ObjectMapper();
            jobList.addAll(mapper.readValue(reader, new TypeReference<List<ImageJob>>() {}));

            System.out.println("Loaded image jobs: " + jobList.size());

        } catch (Exception e) {
            System.err.println("Failed to load image jobs: " + e.getMessage());
        }
    }

    public List<ImageJob> getJobsForImages(List<String> imageIds, String jobType) {
        return jobList.stream()
                .filter(job -> imageIds.contains(job.getImageId()) &&
                        jobType.equalsIgnoreCase(job.getJobType()))
                .collect(Collectors.toList());
    }
}
