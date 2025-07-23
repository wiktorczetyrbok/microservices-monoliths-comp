package pb.java.microservices.rest.search.entity;

import java.util.Objects;

public class NearbyRequest {
    private float lat;
    private float lon;
    private String inDate;
    private String outDate;

    public NearbyRequest() {
    }

    public NearbyRequest(float lat, float lon, String inDate, String outDate) {
        this.lat = lat;
        this.lon = lon;
        this.inDate = inDate;
        this.outDate = outDate;
    }

    // Getters
    public float getLat() {
        return lat;
    }

    public float getLon() {
        return lon;
    }

    public String getInDate() {
        return inDate;
    }

    public String getOutDate() {
        return outDate;
    }

    // Setters
    public void setLat(float lat) {
        this.lat = lat;
    }

    public void setLon(float lon) {
        this.lon = lon;
    }

    public void setInDate(String inDate) {
        this.inDate = inDate;
    }

    public void setOutDate(String outDate) {
        this.outDate = outDate;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        NearbyRequest that = (NearbyRequest) o;
        return Float.compare(that.lat, lat) == 0 &&
                Float.compare(that.lon, lon) == 0 &&
                Objects.equals(inDate, that.inDate) &&
                Objects.equals(outDate, that.outDate);
    }

    @Override
    public int hashCode() {
        return Objects.hash(lat, lon, inDate, outDate);
    }

    @Override
    public String toString() {
        return "NearbyRequest{" +
                "lat=" + lat +
                ", lon=" + lon +
                ", inDate='" + inDate + '\'' +
                ", outDate='" + outDate + '\'' +
                '}';
    }
}
