package pb.java.microservices.monolith.App;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.io.Resource;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.*;
import java.util.*;
import java.util.jar.JarFile;
import java.util.stream.Collectors;

@SpringBootApplication
@RestController
@RequestMapping("/images")
public class AppApplication {

	private static final Map<String, byte[]> imageBuffers = new HashMap<>();
	private static final Map<String, double[]> featureIndex = new HashMap<>();
	private static final Map<String, Metadata> metadataIndex = new HashMap<>();

	private static final ObjectMapper MAPPER = new ObjectMapper();

	public static void main(String[] args) {
		SpringApplication.run(AppApplication.class, args);
	}

	@Bean
	CommandLineRunner loadOnStartup() {
		return args -> loadData();
	}

	private static void loadData() throws Exception {

		loadImages();

		try (
				InputStream f = AppApplication.class.getClassLoader()
						.getResourceAsStream("data/features.json");
				InputStream m = AppApplication.class.getClassLoader()
						.getResourceAsStream("data/metadata.json")
		) {
			if (f == null || m == null) {
				throw new IllegalStateException("Missing JSON resources in classpath");
			}

			List<Feature> features = MAPPER.readValue(
					f, new TypeReference<List<Feature>>() {}
			);
			List<Metadata> metadata = MAPPER.readValue(
					m, new TypeReference<List<Metadata>>() {}
			);

			features.forEach(x -> featureIndex.put(x.id, x.vector));
			metadata.forEach(x -> metadataIndex.put(x.id, x));
			System.out.println(featureIndex);
			System.out.println(metadataIndex);
			System.out.println("Loaded " + imageBuffers.size() + " images");
		}
	}

	private static void loadImages() throws IOException {

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
	}


	@GetMapping("/search")
	public List<MetadataResponse> search(
			@RequestParam(defaultValue = "0.2") double threshold,
			@RequestParam(defaultValue = "3") int kernel
	) {

		String firstImageId = imageBuffers.keySet().iterator().next();
		byte[] queryImage = imageBuffers.get(firstImageId);

		double[] queryVector = extractFeatures(queryImage, kernel);

		List<String> matches = findSimilarImages(queryVector, threshold);

		return matches.isEmpty() ? List.of() : getImageMetadata(matches);
	}

	private static double[] extractFeatures(byte[] imageBuffer, int kernelSize) {

		int[] pixels = new int[imageBuffer.length];
		for (int i = 0; i < imageBuffer.length; i++) {
			pixels[i] = imageBuffer[i] & 0xFF;
		}

		int width = (int) Math.sqrt(pixels.length);
		double[] gray = new double[pixels.length];

		for (int i = 0; i < pixels.length; i++) {
			gray[i] = pixels[i] / 255.0;
		}

		int k = kernelSize * kernelSize;
		double[] kernel = new double[k];
		Arrays.fill(kernel, 1.0 / k);

		double[] output = new double[gray.length];
		int half = kernelSize / 2;

		for (int y = half; y < width - half; y++) {
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
			int idx = Math.min(bins - 1, (int) Math.floor(v * bins));
			hist[idx]++;
		}

		double norm = Math.sqrt(Arrays.stream(hist).map(v -> v * v).sum());
		if (norm == 0) norm = 1;

		for (int i = 0; i < hist.length; i++) {
			hist[i] /= norm;
		}

		return hist;
	}

	private static List<String> findSimilarImages(double[] queryVector, double threshold) {
		return featureIndex.entrySet()
				.stream()
				.filter(e -> euclidean(queryVector, e.getValue()) <= threshold)
				.map(Map.Entry::getKey)
				.collect(Collectors.toList());
	}

	private static double euclidean(double[] a, double[] b) {
		double sum = 0;
		for (int i = 0; i < a.length; i++) {
			double d = a[i] - b[i];
			sum += d * d;
		}
		return Math.sqrt(sum);
	}

	private static List<MetadataResponse> getImageMetadata(List<String> ids) {
		return ids.stream()
				.map(metadataIndex::get)
				.filter(Objects::nonNull)
				.map(m -> new MetadataResponse(m.id, m.name, m.tags))
				.collect(Collectors.toList());
	}

	static class Feature {
		public String id;
		public double[] vector;
	}

	static class Metadata {
		public String id;
		public String name;
		public List<String> tags;
	}

	static class MetadataResponse {
		public String id;
		public String name;
		public List<String> tags;

		MetadataResponse(String id, String name, List<String> tags) {
			this.id = id;
			this.name = name;
			this.tags = tags;
		}
	}
}
