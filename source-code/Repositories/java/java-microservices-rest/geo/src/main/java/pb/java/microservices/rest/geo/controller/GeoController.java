package pb.java.microservices.rest.geo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import pb.java.microservices.rest.geo.service.GeoService;

import java.util.List;

@RestController
public class GeoController {

    @Autowired
    private GeoService geoService;

    @GetMapping("/nearby")
    public List<String> nearbyHotels(
            @RequestParam float lat,
            @RequestParam float lon) {
        return geoService.getNearbyHotels(lat, lon);
    }
}
