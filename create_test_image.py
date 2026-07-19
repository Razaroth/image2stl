"""Test script to create a sample image and test the converter."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

# Create test image directory
test_dir = Path("test_images")
test_dir.mkdir(exist_ok=True)

# Create a simple gradient test image
width, height = 256, 256
data = np.zeros((height, width), dtype=np.uint8)

# Create a gradient from left to right
for x in range(width):
    data[:, x] = int(255 * x / width)

# Create a circle in the center
center_x, center_y = width // 2, height // 2
radius = 80
for y in range(height):
    for x in range(width):
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        if dist <= radius:
            data[y, x] = 255

# Save test image
img = Image.fromarray(data, mode='L')
img.save("test_images/test_gradient.png")

print("✓ Test image created: test_images/test_gradient.png")
print(f"  Size: {width}x{height} pixels")
