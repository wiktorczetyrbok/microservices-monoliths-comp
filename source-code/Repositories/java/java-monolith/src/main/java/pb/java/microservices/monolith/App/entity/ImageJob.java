package pb.java.microservices.monolith.App.entity;

import lombok.Data;

import java.util.Map;


public class ImageJob {
    private String imageId;
    private String jobType; // e.g. "resize", "grayscale"
    private Map<String, Object> parameters;

    // Getters and Setters

    public ImageJob() {
    }


    public String getImageId() {
        return imageId;
    }

    public String getJobType() {
        return jobType;
    }

    public Map<String, Object> getParameters() {
        return parameters;
    }
}
