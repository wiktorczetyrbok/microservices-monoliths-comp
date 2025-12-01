package pb.java.microservices.monolith.App.entity;

import lombok.Data;

import java.util.List;

@Data
public class Hotel {
    private String id;
    private String name;
    private String phoneNumber;
    private String description;
    private Address address;
    private List<Image> images;

}
