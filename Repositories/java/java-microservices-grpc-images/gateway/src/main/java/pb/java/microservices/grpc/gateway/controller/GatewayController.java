package pb.java.microservices.grpc.gateway.controller;

import org.springframework.web.bind.annotation.*;
import pb.java.microservices.grpc.gateway.service.GatewayService;

@RestController
public class GatewayController {

    private final GatewayService gatewayService;

    public GatewayController(GatewayService gatewayService) {
        this.gatewayService = gatewayService;
    }

    @GetMapping("/images/search")
    public Object search(
            @RequestParam(defaultValue = "3") int kernel,
            @RequestParam(defaultValue = "0.9") double threshold) {

        return gatewayService.search(kernel, threshold);
    }
}
