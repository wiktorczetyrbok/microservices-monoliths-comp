package pb.java.microservices.monolith.App.entity;

import lombok.Data;

@Data
public class GeoPoint {
    private String hotelId;
    private double lat;
    private double lon;

}
