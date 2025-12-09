package pb.java.microservices.monolith.App.entity;

import lombok.Data;

public class ImageQuery {
    private String imageId;
    private String jobType;

    public String getImageId() {
        return imageId;
    }

    public ImageQuery() {
    }


    public void setImageId(String imageId) {
        this.imageId = imageId;
    }

    public String getJobType() {
        return jobType;
    }

    public void setJobType(String jobType) {
        this.jobType = jobType;
    }
}
