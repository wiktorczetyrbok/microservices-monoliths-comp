package pb.java.microservices.rest.search.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import pb.java.microservices.rest.search.entity.NearbyRequest;
import pb.java.microservices.rest.search.service.SearchService;

import java.util.List;

@RestController
public class SearchController {

    @Autowired
    private SearchService searchService;

    @PostMapping("/nearby")
    public List<String> searchHotels(
            @RequestBody NearbyRequest body) {


        return searchService.searchNearby(body.getLat(),body.getLon(),body.getInDate(), body.getOutDate());
    }
}

