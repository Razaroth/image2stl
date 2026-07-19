"""Create multiple test images for batch conversion."""
import numpy as np
from PIL import Image
from pathlib import Path

# Create test image directory
test_dir = Path("test_images")
test_dir.mkdir(exist_ok=True)

# Test image 1: Checkerboard
checkerboard = np.zeros((256, 256), dtype=np.uint8)
for i in range(256):
    for j in range(256):
        if (i // 32 + j // 32) % 2 == 0:
            checkerboard[i, j] = 255
img = Image.fromarray(checkerboard)
img.save(test_dir / "checkerboard.png")
print("✓ Created: checkerboard.png")

# Test image 2: Radial gradient
radial = np.zeros((256, 256), dtype=np.uint8)
center = (128, 128)
for i in range(256):
    for j in range(256):
        dist = np.sqrt((i - center[0])**2 + (j - center[1])**2)
        radial[i, j] = min(255, int(dist * 2))
img = Image.fromarray(radial)
img.save(test_dir / "radial.png")
print("✓ Created: radial.png")

# Test image 3: Waves
waves = np.zeros((256, 256), dtype=np.uint8)
for i in range(256):
    for j in range(256):
        val = int(127.5 + 127.5 * np.sin(i / 20) * np.cos(j / 20))
        waves[i, j] = val
img = Image.fromarray(waves)
img.save(test_dir / "waves.png")
print("✓ Created: waves.png")

print("\nReady for batch conversion!")
