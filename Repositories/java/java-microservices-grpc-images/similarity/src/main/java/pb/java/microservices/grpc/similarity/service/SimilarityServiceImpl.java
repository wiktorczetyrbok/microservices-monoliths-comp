package pb.java.microservices.grpc.similarity.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import pb.java.microservices.grpc.similarity.generatedProto.SimilarityGrpc;
import pb.java.microservices.grpc.similarity.generatedProto.SimilarityRequest;
import pb.java.microservices.grpc.similarity.generatedProto.SimilarityResponse;

import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@GrpcService
public class SimilarityServiceImpl extends SimilarityGrpc.SimilarityImplBase {

    private final Map<String, List<Double>> featureIndex = new HashMap<>();

    public SimilarityServiceImpl(ResourceLoader resourceLoader) throws Exception {
        loadFeatures(resourceLoader);
    }

    @Override
    public void find(
            SimilarityRequest request,
            StreamObserver<SimilarityResponse> responseObserver) {

        List<Double> query = request.getQueryVectorList()
                .stream()
                .map(f -> (double) f)
                .collect(Collectors.toList());

        double threshold = request.getThreshold();

        SimilarityResponse.Builder response =
                SimilarityResponse.newBuilder();

        for (Map.Entry<String, List<Double>> entry : featureIndex.entrySet()) {
            double dist = euclidean(query, entry.getValue());
            System.out.printf("[SIM] %s dist=%.4f%n", entry.getKey(), dist);
            if (dist <= threshold) {
                response.addImageIds(entry.getKey());
            }
        }

        responseObserver.onNext(response.build());
        responseObserver.onCompleted();
    }

    private void loadFeatures(ResourceLoader resourceLoader) throws Exception {
        Resource resource = resourceLoader.getResource("classpath:data/features.json");
        ObjectMapper mapper = new ObjectMapper();
        try (InputStream is = resource.getInputStream()) {
            List<Map<String, Object>> features =
                    mapper.readValue(is, new TypeReference<>() {});
            for (Map<String, Object> f : features) {
                String id = (String) f.get("id");
                @SuppressWarnings("unchecked")
                List<Double> vector = (List<Double>) f.get("vector");
                featureIndex.put(id, vector);
            }
        }
    }

    private double euclidean(List<Double> a, List<Double> b) {
        double sum = 0;
        for (int i = 0; i < a.size(); i++) {
            double d = a.get(i) - b.get(i);
            sum += d * d;
        }
        return Math.sqrt(sum);
    }
}
