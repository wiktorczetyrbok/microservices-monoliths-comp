package pb.java.microservices.monolith.App.entity;

import lombok.Data;

@Data
public class Address {
    private String streetNumber;
    private String streetName;
    private String city;
    private String state;
    private String country;
    private String postalCode;
    private Float lat;
    private Float lon;

}
