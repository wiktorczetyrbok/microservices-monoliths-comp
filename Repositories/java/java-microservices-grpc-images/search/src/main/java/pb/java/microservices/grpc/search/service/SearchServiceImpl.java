package pb.java.microservices.grpc.search.service;

import io.grpc.ManagedChannel;
import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import pb.java.microservices.grpc.feature.generatedProto.FeatureGrpc;
import pb.java.microservices.grpc.feature.generatedProto.FeatureRequest;
import pb.java.microservices.grpc.similarity.generatedProto.SimilarityGrpc;
import pb.java.microservices.grpc.similarity.generatedProto.SimilarityRequest;
import pb.java.microservices.grpc.search.generatedProto.SearchGrpc;
import pb.java.microservices.grpc.search.generatedProto.SearchRequest;
import pb.java.microservices.grpc.search.generatedProto.SearchResponse;

@GrpcService
public class SearchServiceImpl extends SearchGrpc.SearchImplBase {

    @Autowired
    @Qualifier("FeatureServiceChannel")
    private ManagedChannel featureServiceChannel;

    @Autowired
    @Qualifier("SimilarityServiceChannel")
    private ManagedChannel similarityServiceChannel;

    @Override
    public void search(
            SearchRequest request,
            StreamObserver<SearchResponse> responseObserver) {

        FeatureGrpc.FeatureBlockingStub featureStub =
                FeatureGrpc.newBlockingStub(featureServiceChannel);

        SimilarityGrpc.SimilarityBlockingStub similarityStub =
                SimilarityGrpc.newBlockingStub(similarityServiceChannel);

        var featureResponse =
                featureStub.extract(
                        FeatureRequest.newBuilder()
                                .setImageId("img001")
                                .setKernel(request.getKernel())
                                .build()
                );

        var similarityResponse =
                similarityStub.find(
                        SimilarityRequest.newBuilder()
                                .addAllQueryVector(featureResponse.getVectorList())
                                .setThreshold(request.getThreshold())
                                .build()
                );

        SearchResponse response =
                SearchResponse.newBuilder()
                        .addAllImageIds(similarityResponse.getImageIdsList())
                        .build();

        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}
