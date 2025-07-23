package pb.java.microservices.rest.gateway.entity;

import lombok.Data;

import java.util.List;

@Data
public class Request {
    private List<String> hotelIds;
}
