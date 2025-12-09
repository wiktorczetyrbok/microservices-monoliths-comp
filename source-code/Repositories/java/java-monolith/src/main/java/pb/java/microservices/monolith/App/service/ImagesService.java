package pb.java.microservices.monolith.App.service;

import jakarta.annotation.PostConstruct;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;
import pb.java.microservices.monolith.App.entity.ImageMeta;
import pb.java.microservices.monolith.App.entity.ImageQuery;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.InputStream;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class ImagesService {

    private final GeoImageService geoImageService;
    private final MetaService metaService;
    private final JobService jobService;
    private final ResourceLoader resourceLoader;

    public ImagesService(GeoImageService geoImageService,
                         MetaService metaService,
                         JobService jobService,
                         ResourceLoader resourceLoader) {
        this.geoImageService = geoImageService;
        this.metaService = metaService;
        this.jobService = jobService;
        this.resourceLoader = resourceLoader;
    }

    public List<Map<String, Object>> searchImages(float lat, float lon, String jobType) {
        List<String> imageIds = geoImageService.getNearbyImageIds(lat, lon);
        List<ImageMeta> metas = metaService.getMetadata(imageIds);
        List<ImageQuery> jobs = jobService.getJobsForImages(imageIds, jobType).stream()
                .map(job -> {
                    ImageQuery query = new ImageQuery();
                    query.setImageId(job.getImageId());
                    query.setJobType(job.getJobType());
                    return query;
                })
                .toList();
        return jobs.stream().map(job -> {
            Map<String, Object> result = new LinkedHashMap<>();
            ImageMeta meta = metas.stream()
                    .filter(m -> m.getId().equals(job.getImageId()))
                    .findFirst().orElse(null);

            if (meta == null) return null;

            result.put("imageId", meta.getId());
            result.put("name", meta.getName());
            result.put("jobType", jobType);

            try {
                BufferedImage img = loadBufferedImage(meta.getUrl());
                long start = System.nanoTime();
                Object jobResult = processJob(img, jobType);
                long end = System.nanoTime();

                result.put("processingTimeMs", (end - start) / 1_000_000);

                if (jobResult instanceof Double entropy) {
                    result.put("entropy", entropy);
                }

            } catch (Exception e) {
                result.put("error", e.getMessage());
            }

            return result;
        }).filter(Objects::nonNull).collect(Collectors.toList());
    }

    private BufferedImage loadBufferedImage(String url) throws Exception {
        if (!url.startsWith("classpath:")) {
            throw new IllegalArgumentException("Unsupported image URL: " + url);
        }
        Resource resource = resourceLoader.getResource(url);
        try (InputStream is = resource.getInputStream()) {
            return ImageIO.read(is);
        }
    }

    private Object processJob(BufferedImage img, String jobType) {
        return switch (jobType) {
            case "resize" -> resize(img, 100, 100);
            case "invert" -> invert(img);
            case "grayscale" -> toGrayscale(img);
            case "blur" -> blur(img);
            case "entropy" -> computeEntropy(img);
            default -> throw new IllegalArgumentException("Unknown jobType: " + jobType);
        };
    }

    private BufferedImage resize(BufferedImage original, int width, int height) {
        BufferedImage resized = new BufferedImage(width, height, original.getType());
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int srcX = x * original.getWidth() / width;
                int srcY = y * original.getHeight() / height;
                resized.setRGB(x, y, original.getRGB(srcX, srcY));
            }
        }
        return resized;
    }

    private BufferedImage invert(BufferedImage original) {
        BufferedImage inverted = new BufferedImage(original.getWidth(), original.getHeight(), original.getType());
        for (int y = 0; y < original.getHeight(); y++) {
            for (int x = 0; x < original.getWidth(); x++) {
                int rgb = original.getRGB(x, y);
                int r = 255 - ((rgb >> 16) & 0xFF);
                int g = 255 - ((rgb >> 8) & 0xFF);
                int b = 255 - (rgb & 0xFF);
                int newRGB = (0xFF << 24) | (r << 16) | (g << 8) | b;
                inverted.setRGB(x, y, newRGB);
            }
        }
        return inverted;
    }

    private BufferedImage toGrayscale(BufferedImage original) {
        BufferedImage gray = new BufferedImage(original.getWidth(), original.getHeight(), original.getType());
        for (int y = 0; y < original.getHeight(); y++) {
            for (int x = 0; x < original.getWidth(); x++) {
                int rgb = original.getRGB(x, y);
                int r = (rgb >> 16) & 0xFF;
                int g = (rgb >> 8) & 0xFF;
                int b = rgb & 0xFF;
                int avg = (r + g + b) / 3;
                int grayRGB = (0xFF << 24) | (avg << 16) | (avg << 8) | avg;
                gray.setRGB(x, y, grayRGB);
            }
        }
        return gray;
    }

    private BufferedImage blur(BufferedImage img) {
        int w = img.getWidth();
        int h = img.getHeight();
        BufferedImage out = new BufferedImage(w, h, img.getType());

        for (int y = 1; y < h - 1; y++) {
            for (int x = 1; x < w - 1; x++) {
                int r = 0, g = 0, b = 0;
                for (int dy = -1; dy <= 1; dy++) {
                    for (int dx = -1; dx <= 1; dx++) {
                        int rgb = img.getRGB(x + dx, y + dy);
                        r += (rgb >> 16) & 0xFF;
                        g += (rgb >> 8) & 0xFF;
                        b += rgb & 0xFF;
                    }
                }
                r /= 9;
                g /= 9;
                b /= 9;
                int blurredRGB = (0xFF << 24) | (r << 16) | (g << 8) | b;
                out.setRGB(x, y, blurredRGB);
            }
        }
        return out;
    }

    private double computeEntropy(BufferedImage img) {
        int[] histogram = new int[256];
        int w = img.getWidth();
        int h = img.getHeight();

        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                int rgb = img.getRGB(x, y);
                int gray = ((rgb >> 16) & 0xFF + (rgb >> 8) & 0xFF + (rgb & 0xFF)) / 3;
                histogram[gray]++;
            }
        }

        double entropy = 0.0;
        int totalPixels = w * h;
        for (int freq : histogram) {
            if (freq > 0) {
                double p = freq / (double) totalPixels;
                entropy -= p * Math.log(p) / Math.log(2);
            }
        }
        return entropy;
    }
}
