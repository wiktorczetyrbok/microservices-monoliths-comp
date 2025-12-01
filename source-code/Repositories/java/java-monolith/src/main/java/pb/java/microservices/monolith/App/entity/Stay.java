package pb.java.microservices.monolith.App.entity;

import java.util.Objects;

public class Stay {
    private final String inDate;
    private final String outDate;
    private String hotelId;

    public Stay(String hotelId, String inDate, String outDate) {
        this.hotelId = hotelId;
        this.inDate = inDate;
        this.outDate = outDate;
    }

    public String getHotelId() {
        return hotelId;
    }

    public void setHotelId(String hotelId) {
        this.hotelId = hotelId;
    }

}
