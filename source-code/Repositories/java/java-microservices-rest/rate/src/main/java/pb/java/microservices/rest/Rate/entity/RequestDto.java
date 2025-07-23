package pb.java.microservices.rest.Rate.entity;

import java.util.List;

public class RequestDto {
    public List<String> getHotelIds() {
        return hotelIds;
    }

    public void setHotelIds(List<String> hotelIds) {
        this.hotelIds = hotelIds;
    }

    public String getInDate() {
        return inDate;
    }

    public void setInDate(String inDate) {
        this.inDate = inDate;
    }

    public String getOutDate() {
        return outDate;
    }

    public void setOutDate(String outDate) {
        this.outDate = outDate;
    }

    private List<String> hotelIds;
    private String inDate;
    private String outDate;
    // Add other fields as needed

    public RequestDto() {
        // Default constructor
    }

    public RequestDto(List<String> hotelIds, String inDate, String outDate) {
        this.hotelIds = hotelIds;
        this.inDate = inDate;
        this.outDate = outDate;
    }

    // Add getters and setters for the fields
}

