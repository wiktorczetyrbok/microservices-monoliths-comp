package pb.java.microservices.monolith.App.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import pb.java.microservices.monolith.App.service.HotelsService;

import java.util.Map;

@RestController
public class HotelsController {

    @Autowired
    private HotelsService hotelsService;

    @RequestMapping("/hotels")
    public Map<String, Object> searchHandler(
            @RequestParam(value = "inDate") String inDate,
            @RequestParam(value = "outDate") String outDate,
            @RequestParam(value = "lat") float lat,
            @RequestParam(value = "lon") float lon) {

        return hotelsService.searchHotels(inDate, outDate, lat, lon);
    }
}