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

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Stay stay = (Stay) o;
        return Objects.equals(hotelId, stay.hotelId) && Objects.equals(inDate, stay.inDate) && Objects.equals(outDate, stay.outDate);
    }

    @Override
    public int hashCode() {
        return Objects.hash(hotelId, inDate, outDate);
    }

    public String getHotelId() {
        return hotelId;
    }

    public void setHotelId(String hotelId) {
        this.hotelId = hotelId;
    }

}
