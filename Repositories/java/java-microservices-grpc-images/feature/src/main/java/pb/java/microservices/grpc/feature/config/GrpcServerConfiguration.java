package pb.java.microservices.grpc.feature.config;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import pb.java.microservices.grpc.feature.service.FeatureServiceImpl;

import java.io.IOException;

@Configuration
public class GrpcServerConfiguration {

    @Bean
    public Server grpcServer(FeatureServiceImpl featureService) throws IOException {
        Server server = ServerBuilder
                .forPort(8080)
                .addService(featureService)
                .build();
        server.start();
        return server;
    }
}
