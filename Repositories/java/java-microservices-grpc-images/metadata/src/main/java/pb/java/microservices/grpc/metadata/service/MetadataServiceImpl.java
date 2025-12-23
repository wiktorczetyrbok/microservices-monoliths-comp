package pb.java.microservices.grpc.metadata.service;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import com.google.protobuf.util.JsonFormat;
import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.util.FileCopyUtils;
import pb.java.microservices.grpc.metadata.generatedProto.ImageMeta;
import pb.java.microservices.grpc.metadata.generatedProto.MetadataGrpc;
import pb.java.microservices.grpc.metadata.generatedProto.MetadataRequest;
import pb.java.microservices.grpc.metadata.generatedProto.MetadataResponse;

import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

@GrpcService
public class MetadataServiceImpl extends MetadataGrpc.MetadataImplBase {

    private final Map<String, ImageMeta> metadataIndex = new HashMap<>();
    private final ResourceLoader resourceLoader;

    @Autowired
    public MetadataServiceImpl(ResourceLoader resourceLoader) throws IOException {
        this.resourceLoader = resourceLoader;
        loadMetadataFromJson("data/metadata.json");
    }

    @Override
    public void get(
            MetadataRequest request,
            StreamObserver<MetadataResponse> responseObserver) {

        MetadataResponse.Builder response =
                MetadataResponse.newBuilder();

        for (String id : request.getImageIdsList()) {
            ImageMeta meta = metadataIndex.get(id);
            if (meta != null) {
                response.addImages(meta);
            }
        }

        responseObserver.onNext(response.build());
        responseObserver.onCompleted();
    }

    private void loadMetadataFromJson(String filename) throws IOException {
        String json = readJsonFile(filename);
        JsonArray array = JsonParser.parseString(json).getAsJsonArray();

        ImageMeta.Builder builder = ImageMeta.newBuilder();
        for (JsonElement el : array) {
            JsonFormat.parser()
                    .ignoringUnknownFields()
                    .merge(el.toString(), builder);
            metadataIndex.put(builder.getId(), builder.build());
            builder.clear();
        }

        System.out.println(
                "[METADATA] Loaded " + metadataIndex.size() + " records"
        );
    }

    private String readJsonFile(String filename) throws IOException {
        Resource resource = resourceLoader.getResource("classpath:" + filename);
        InputStreamReader reader =
                new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8);
        return FileCopyUtils.copyToString(reader);
    }
}
