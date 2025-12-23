package pb.java.microservices.grpc.gateway.service;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import org.springframework.stereotype.Service;
import com.google.protobuf.util.JsonFormat;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;
import java.util.Map;
import pb.java.microservices.grpc.search.generatedProto.SearchGrpc;
import pb.java.microservices.grpc.search.generatedProto.SearchRequest;
import pb.java.microservices.grpc.search.generatedProto.SearchResponse;
import pb.java.microservices.grpc.metadata.generatedProto.MetadataGrpc;
import pb.java.microservices.grpc.metadata.generatedProto.MetadataRequest;
import pb.java.microservices.grpc.metadata.generatedProto.MetadataResponse;

@Service
public class GatewayService {

    private final SearchGrpc.SearchBlockingStub searchClient;
    private final MetadataGrpc.MetadataBlockingStub metadataClient;

    public GatewayService() {

        ManagedChannel searchChannel =
                ManagedChannelBuilder.forTarget("search:8080")
                        .usePlaintext()
                        .build();

        ManagedChannel metadataChannel =
                ManagedChannelBuilder.forTarget("metadata:8080")
                        .usePlaintext()
                        .build();

        this.searchClient = SearchGrpc.newBlockingStub(searchChannel);
        this.metadataClient = MetadataGrpc.newBlockingStub(metadataChannel);
    }

    public Object search(int kernel, double threshold) {

        SearchResponse searchRes =
                searchClient.search(
                        SearchRequest.newBuilder()
                                .setKernel(kernel)
                                .setThreshold((float) threshold)
                                .build()
                );

        if (searchRes.getImageIdsList().isEmpty()) {
            return List.of();
        }

        MetadataResponse metaRes =
                metadataClient.get(
                        MetadataRequest.newBuilder()
                                .addAllImageIds(searchRes.getImageIdsList())
                                .build()
                );

        try {
            // 1. protobuf → JSON string (NO unknownFields)
            String json =
                    JsonFormat.printer()
                            .omittingInsignificantWhitespace()
                            .print(metaRes);

            // 2. JSON string → plain Java Map/List
            ObjectMapper mapper = new ObjectMapper();
            Map<String, Object> parsed = mapper.readValue(json, Map.class);

            // 3. return ONLY images (matches JS behavior)
            return parsed.get("images");

        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
