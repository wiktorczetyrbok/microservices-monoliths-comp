package pb.java.microservices.rest.profile.entity;

import java.util.List;

public class Hotel {
    private String id;
    private String name;
    private String phoneNumber;
    private String description;
    private Address address;
    private List<Image> images;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Address getAddress() {
        return address;
    }

    public void setAddress(Address address) {
        this.address = address;
    }

    public List<Image> getImages() {
        return images;
    }

    public void setImages(List<Image> images) {
        this.images = images;
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private String id;
        private String name;
        private String phoneNumber;
        private String description;
        private Address address;
        private List<Image> images;

        public Builder id(String id) {
            this.id = id;
            return this;
        }

        public Builder name(String name) {
            this.name = name;
            return this;
        }

        public Builder phoneNumber(String phoneNumber) {
            this.phoneNumber = phoneNumber;
            return this;
        }

        public Builder description(String description) {
            this.description = description;
            return this;
        }

        public Builder address(Address address) {
            this.address = address;
            return this;
        }

        public Builder images(List<Image> images) {
            this.images = images;
            return this;
        }

        public Hotel build() {
            Hotel hotel = new Hotel();
            hotel.id = this.id;
            hotel.name = this.name;
            hotel.phoneNumber = this.phoneNumber;
            hotel.description = this.description;
            hotel.address = this.address;
            hotel.images = this.images;
            return hotel;
        }
    }
}
