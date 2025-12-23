package pb.java.microservices.grpc.metadata.config;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import pb.java.microservices.grpc.metadata.service.MetadataServiceImpl;

import java.io.IOException;

@Configuration
public class GrpcServerConfiguration {

    @Bean
    public Server grpcServer(MetadataServiceImpl metadataService)
            throws IOException {

        Server server = ServerBuilder
                .forPort(8080)
                .addService(metadataService)
                .build();

        server.start();
        return server;
    }
}
