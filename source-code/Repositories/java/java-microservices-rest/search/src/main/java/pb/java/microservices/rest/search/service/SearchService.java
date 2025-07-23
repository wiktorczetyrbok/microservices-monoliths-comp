package pb.java.microservices.rest.search.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import pb.java.microservices.rest.search.entity.RatePlan;
import pb.java.microservices.rest.search.entity.RateRequestDto;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class SearchService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${geo.service.path}")
    private String geoServiceEndpoint;

    @Value("${rate.service.path}")
    private String rateServiceEndpoint;

    public List<String> searchNearby(float lat, float lon, String inDate, String outDate) {

        // Making REST call to geo service
        ResponseEntity<List<String>> geoResponse = restTemplate.exchange(
                geoServiceEndpoint + "?lat=" + lat + "&lon=" + lon,
                HttpMethod.GET,
                null,
                new ParameterizedTypeReference<List<String>>() {}
        );
        List<String> geoHotelIds = geoResponse.getBody();

        // Constructing the body for rate service
        RateRequestDto rateRequestDto = new RateRequestDto(geoHotelIds, inDate, outDate);

        // Making REST call to rate service
        ResponseEntity<List<RatePlan>> rateResponse = restTemplate.exchange(
                rateServiceEndpoint,
                HttpMethod.POST,
                new HttpEntity<>(rateRequestDto),
                new ParameterizedTypeReference<List<RatePlan>>() {}
        );

        // Extracting hotelIds from RatePlans and returning
        return rateResponse.getBody().stream().map(RatePlan::getHotelId).collect(Collectors.toList());
    }
}
