package pb.java.microservices.rest.search.entity;

import java.util.List;

public class RateRequestDto {
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

    public RateRequestDto() {
        // Default constructor
    }

    public RateRequestDto(List<String> hotelIds, String inDate, String outDate) {
        this.hotelIds = hotelIds;
        this.inDate = inDate;
        this.outDate = outDate;
    }

    // Add getters and setters for the fields
}

