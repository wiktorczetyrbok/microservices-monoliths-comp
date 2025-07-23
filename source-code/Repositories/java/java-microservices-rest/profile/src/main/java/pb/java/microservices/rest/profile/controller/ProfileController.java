package pb.java.microservices.rest.profile.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import pb.java.microservices.rest.profile.entity.Hotel;
import pb.java.microservices.rest.profile.service.ProfileService;

import java.util.List;

@RestController
public class ProfileController {

    private final ProfileService profileService;

    public ProfileController(ProfileService profileService) {
        this.profileService = profileService;
    }

    @PostMapping("/hotels")
    public List<Hotel> getProfiles(@RequestBody List<String> hotelIds) {
        return profileService.getProfiles(hotelIds);
    }
}
