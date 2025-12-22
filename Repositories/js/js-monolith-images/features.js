export function extractFeatures(imageBuffer, kernelSize = 3) {
    const pixels = [...imageBuffer];
    const width = Math.sqrt(pixels.length) | 0;
    const height = width;

    // Grayscale
    const gray = new Array(pixels.length);
    for (let i = 0; i < pixels.length; i++) {
        gray[i] = pixels[i] / 255;
    }

    // Simple convolution kernel
    const kernel = new Array(kernelSize * kernelSize).fill(
        1 / (kernelSize * kernelSize)
    );

    const output = new Array(gray.length).fill(0);
    const half = Math.floor(kernelSize / 2);

    for (let y = half; y < height - half; y++) {
        for (let x = half; x < width - half; x++) {
            let sum = 0;
            for (let ky = -half; ky <= half; ky++) {
                for (let kx = -half; kx <= half; kx++) {
                    const px =
                        (y + ky) * width + (x + kx);
                    sum +=
                        gray[px] *
                        kernel[(ky + half) * kernelSize + (kx + half)];
                }
            }
            output[y * width + x] = sum;
        }
    }

    // Histogram (feature vector)
    const bins = 16;
    const hist = new Array(bins).fill(0);

    output.forEach(v => {
        const idx = Math.min(
            bins - 1,
            Math.floor(v * bins)
        );
        hist[idx]++;
    });

    // Normalize
    const norm =
        Math.sqrt(hist.reduce((s, v) => s + v * v, 0)) || 1;

    return hist.map(v => v / norm);
}
