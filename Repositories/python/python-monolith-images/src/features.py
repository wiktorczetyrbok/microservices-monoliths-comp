import math


def extract_features(image_buffer: bytes, kernel_size: int = 3):
    pixels = list(image_buffer)

    width = int(math.sqrt(len(pixels)))
    height = width
    # Grayscale
    gray = [p / 255.0 for p in pixels]

    kernel_value = 1.0 / (kernel_size * kernel_size)
    kernel = [kernel_value] * (kernel_size * kernel_size)

    output = [0.0] * len(gray)
    half = kernel_size // 2

    for y in range(half, height - half):
        for x in range(half, width - half):
            s = 0.0
            for ky in range(-half, half + 1):
                for kx in range(-half, half + 1):
                    px = (y + ky) * width + (x + kx)
                    s += gray[px] * kernel[
                        (ky + half) * kernel_size + (kx + half)
                        ]
            output[y * width + x] = s

    # Histogram features
    bins = 16
    hist = [0] * bins
    for v in output:
        idx = min(bins - 1, int(math.floor(v * bins)))
        hist[idx] += 1

    # Normalize
    norm = math.sqrt(sum(v * v for v in hist)) or 1.0
    return [v / norm for v in hist]
