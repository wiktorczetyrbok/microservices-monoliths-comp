package pb.java.microservices.grpc.search.config;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

@Component
public class SimilarityServiceChannel {

    @Bean
    public ManagedChannel SimilarityServiceChannel() {
        return ManagedChannelBuilder
                .forTarget("similarity:8080")
                .usePlaintext()
                .build();
    }
}
