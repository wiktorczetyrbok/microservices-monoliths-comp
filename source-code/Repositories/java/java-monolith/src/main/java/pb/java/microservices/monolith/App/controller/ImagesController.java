package pb.java.microservices.monolith.App.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import pb.java.microservices.monolith.App.service.ImagesService;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/images")
public class ImagesController {

    @Autowired
    private ImagesService imagesService;

    @GetMapping("/search")
    public List<Map<String, Object>> searchImages(
            @RequestParam float lat,
            @RequestParam float lon,
            @RequestParam String jobType) {
        return imagesService.searchImages(lat, lon, jobType);
    }
}