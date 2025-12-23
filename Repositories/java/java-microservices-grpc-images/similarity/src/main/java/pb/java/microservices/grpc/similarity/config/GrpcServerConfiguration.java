package pb.java.microservices.grpc.similarity.config;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import pb.java.microservices.grpc.similarity.service.SimilarityServiceImpl;

@Configuration
public class GrpcServerConfiguration {

    @Bean
    public Server grpcServer(SimilarityServiceImpl similarityService) throws Exception {
        Server server = ServerBuilder
                .forPort(8080)
                .addService(similarityService)
                .build();
        server.start();
        return server;
    }
}
