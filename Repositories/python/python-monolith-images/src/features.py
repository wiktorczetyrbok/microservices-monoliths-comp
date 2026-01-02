import math


def extract_features(image_bytes: bytes, kernel_size: int = 3):
    pixels = list(image_bytes)

    size = int(math.sqrt(len(pixels)))
    width = height = size

    gray = [p / 255.0 for p in pixels]

    k = kernel_size
    half = k // 2
    output = [0.0] * len(gray)

    for y in range(half, height - half):
        for x in range(half, width - half):
            acc = 0.0
            for ky in range(-half, half + 1):
                for kx in range(-half, half + 1):
                    px = (y + ky) * width + (x + kx)
                    acc += gray[px]
            output[y * width + x] = acc / (k * k)

    bins = 16
    hist = [0] * bins

    for v in output:
        idx = min(bins - 1, int(v * bins))
        hist[idx] += 1

    norm = math.sqrt(sum(v * v for v in hist)) or 1.0
    return [v / norm for v in hist]

