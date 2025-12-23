package pb.java.microservices.grpc.feature.service;

import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import pb.java.microservices.grpc.feature.generatedProto.FeatureGrpc;
import pb.java.microservices.grpc.feature.generatedProto.FeatureRequest;
import pb.java.microservices.grpc.feature.generatedProto.FeatureResponse;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.*;

@GrpcService
public class FeatureServiceImpl extends FeatureGrpc.FeatureImplBase {

    private final Map<String, byte[]> imageBuffers = new HashMap<>();

    public FeatureServiceImpl(ResourceLoader resourceLoader) throws IOException {
        loadImages();
    }

    @Override
    public void extract(
            FeatureRequest request,
            StreamObserver<FeatureResponse> responseObserver) {

        byte[] buffer = imageBuffers.get(request.getImageId());

        if (buffer == null) {
            responseObserver.onNext(
                    FeatureResponse.newBuilder().build()
            );
            responseObserver.onCompleted();
            return;
        }

        List<Float> vector =
                extractFeatures(buffer, request.getKernel());

        FeatureResponse response =
                FeatureResponse.newBuilder()
                        .addAllVector(vector)
                        .build();

        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    private void loadImages() throws IOException {

        var resolver = new PathMatchingResourcePatternResolver();
        Resource[] resources = resolver.getResources("classpath:data/images/*");

        for (Resource resource : resources) {
            if (!resource.isReadable()) continue;

            String filename = resource.getFilename();
            if (filename == null) continue;

            String id = filename;
            int dot = id.lastIndexOf('.');
            if (dot > 0) {
                id = id.substring(0, dot);
            }

            imageBuffers.put(id, resource.getInputStream().readAllBytes());
        }
        System.out.println("Loaded " + imageBuffers.size() + " images");
    }

    private List<Float> extractFeatures(byte[] image, int kernelSize) {

        int size = (int) Math.sqrt(image.length);
        int width = size;
        int height = size;

        double[] gray = new double[image.length];
        for (int i = 0; i < image.length; i++) {
            gray[i] = (image[i] & 0xFF) / 255.0;
        }

        double[] kernel = new double[kernelSize * kernelSize];
        Arrays.fill(kernel, 1.0 / kernel.length);

        double[] output = new double[gray.length];
        int half = kernelSize / 2;

        for (int y = half; y < height - half; y++) {
            for (int x = half; x < width - half; x++) {
                double sum = 0;
                for (int ky = -half; ky <= half; ky++) {
                    for (int kx = -half; kx <= half; kx++) {
                        int px = (y + ky) * width + (x + kx);
                        sum += gray[px] *
                                kernel[(ky + half) * kernelSize + (kx + half)];
                    }
                }
                output[y * width + x] = sum;
            }
        }

        int bins = 16;
        double[] hist = new double[bins];

        for (double v : output) {
            int idx = Math.min(bins - 1, (int) (v * bins));
            hist[idx]++;
        }

        double norm = 0;
        for (double v : hist) norm += v * v;
        norm = Math.sqrt(norm);
        if (norm == 0) norm = 1;

        List<Float> result = new ArrayList<>();
        for (double v : hist) {
            result.add((float) (v / norm));
        }

        return result;
    }
}
