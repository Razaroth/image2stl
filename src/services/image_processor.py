"""Image processing module for image to STL conversion."""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from scipy import ndimage


class ImageProcessor:
    """Handle image loading and preprocessing."""

    @staticmethod
    def load_image(image_path: str, grayscale: bool = True) -> np.ndarray:
        """
        Load image from file.

        Args:
            image_path: Path to the image file
            grayscale: Convert to grayscale (default: True)

        Returns:
            Numpy array representing the image (0-255)
        """
        img = Image.open(image_path)
        
        if grayscale:
            img = img.convert('L')
        
        return np.array(img, dtype=np.uint8)

    @staticmethod
    def resize_image(image_array: np.ndarray, max_dimension: int = 512) -> np.ndarray:
        """
        Resize image to manageable size while maintaining aspect ratio.

        Args:
            image_array: Input image as numpy array
            max_dimension: Maximum width/height

        Returns:
            Resized image array
        """
        height, width = image_array.shape[:2]
        
        if max(height, width) > max_dimension:
            scale = max_dimension / max(height, width)
            new_size = (int(width * scale), int(height * scale))
            img = Image.fromarray(image_array)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            return np.array(img, dtype=np.uint8)
        
        return image_array

    @staticmethod
    def normalize_image(image_array: np.ndarray) -> np.ndarray:
        """
        Normalize image to 0-1 range.

        Args:
            image_array: Input image array (0-255)

        Returns:
            Normalized image array (0-1)
        """
        return image_array.astype(np.float32) / 255.0

    @staticmethod
    def apply_smoothing(image_array: np.ndarray, sigma: float = 1.0) -> np.ndarray:
        """
        Apply Gaussian smoothing to reduce noise.

        Args:
            image_array: Input image array (0-1)
            sigma: Standard deviation for Gaussian kernel

        Returns:
            Smoothed image array
        """
        return ndimage.gaussian_filter(image_array, sigma=sigma)

    @staticmethod
    def invert_image(image_array: np.ndarray) -> np.ndarray:
        """
        Invert image values (0-1).

        Args:
            image_array: Input image array (0-1)

        Returns:
            Inverted image array
        """
        return 1.0 - image_array

    @staticmethod
    def adjust_contrast(image_array: np.ndarray, contrast_factor: float = 1.5) -> np.ndarray:
        """
        Adjust image contrast.

        Args:
            image_array: Input image array (0-255)
            contrast_factor: Factor > 1 increases contrast, < 1 decreases

        Returns:
            Contrast-adjusted image array (0-255)
        """
        img = Image.fromarray(image_array.astype(np.uint8))
        enhancer = ImageEnhance.Contrast(img)
        enhanced = enhancer.enhance(contrast_factor)
        return np.array(enhanced, dtype=np.uint8)

    @staticmethod
    def adjust_brightness(image_array: np.ndarray, brightness_factor: float = 1.0) -> np.ndarray:
        """
        Adjust image brightness.

        Args:
            image_array: Input image array (0-255)
            brightness_factor: Factor > 1 increases brightness, < 1 decreases

        Returns:
            Brightness-adjusted image array (0-255)
        """
        img = Image.fromarray(image_array.astype(np.uint8))
        enhancer = ImageEnhance.Brightness(img)
        enhanced = enhancer.enhance(brightness_factor)
        return np.array(enhanced, dtype=np.uint8)

    @staticmethod
    def detect_edges(image_array: np.ndarray, mode: str = "sobel") -> np.ndarray:
        """
        Detect edges in the image.

        Args:
            image_array: Input image array (0-1)
            mode: Edge detection mode - "sobel", "laplace", or "canny"

        Returns:
            Edge-detected image array (0-1)
        """
        if mode == "sobel":
            edges_x = ndimage.sobel(image_array, axis=0)
            edges_y = ndimage.sobel(image_array, axis=1)
            edges = np.sqrt(edges_x**2 + edges_y**2)
        elif mode == "laplace":
            edges = ndimage.laplace(image_array)
            edges = np.abs(edges)
        elif mode == "canny":
            # Use Canny edge detection from scipy
            img_255 = (image_array * 255).astype(np.uint8)
            img_pil = Image.fromarray(img_255)
            edges_img = img_pil.filter(ImageFilter.FIND_EDGES)
            edges = np.array(edges_img, dtype=np.float32) / 255.0
            return edges
        else:
            raise ValueError(f"Unknown edge detection mode: {mode}")
        
        # Normalize to 0-1
        edges = edges - edges.min()
        if edges.max() > 0:
            edges = edges / edges.max()
        
        return edges

    @staticmethod
    def equalize_histogram(image_array: np.ndarray) -> np.ndarray:
        """
        Equalize image histogram for better contrast.

        Args:
            image_array: Input image array (0-255)

        Returns:
            Histogram-equalized image array (0-255)
        """
        img = Image.fromarray(image_array.astype(np.uint8))
        return np.array(ImageEnhance.Contrast(img).enhance(2.0), dtype=np.uint8)
