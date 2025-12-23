package pb.java.microservices.grpc.search.config;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

@Component
public class FeatureServiceChannel {

    @Bean
    public ManagedChannel FeatureServiceChannel() {
        return ManagedChannelBuilder
                .forTarget("feature:8080")
                .usePlaintext()
                .build();
    }
}
