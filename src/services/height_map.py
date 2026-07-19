"""Height map generation from images."""

import numpy as np
from enum import Enum


class HeightMapMode(Enum):
    """Height map generation modes."""
    GRAYSCALE = "grayscale"
    INVERTED = "inverted"
    EDGE_BASED = "edge_based"
    COLOR_TO_HEIGHT = "color_to_height"


class HeightMapGenerator:
    """Generate 3D height maps from 2D images."""

    @staticmethod
    def generate_height_map(
        image_array: np.ndarray,
        max_height: float = 10.0,
        scale_xy: float = 100.0,
        resolution: float = 1.0,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate 3D height map from image.

        Args:
            image_array: Normalized image array (0-1)
            max_height: Maximum height in mm
            scale_xy: XY scale factor
            resolution: Resolution factor (lower = more detailed)

        Returns:
            Tuple of (X, Y, Z) mesh grids
        """
        # Apply resolution downsampling
        step = max(1, int(resolution))
        
        height, width = image_array.shape
        
        # Scale coordinates
        x = np.arange(0, width, step) * (scale_xy / width)
        y = np.arange(0, height, step) * (scale_xy / height)
        
        # Downsample image if needed
        if step > 1:
            z = image_array[::step, ::step]
        else:
            z = image_array
        
        # Create mesh grid
        X, Y = np.meshgrid(x, y)
        
        # Scale Z to height range
        Z = z * max_height
        
        return X, Y, Z

    @staticmethod
    def apply_base_thickness(Z: np.ndarray, base_thickness: float = 2.0) -> np.ndarray:
        """
        Add base thickness to prevent model from being too thin.

        Args:
            Z: Height array
            base_thickness: Minimum thickness in mm

        Returns:
            Height array with base thickness added
        """
        return Z + base_thickness

    @staticmethod
    def smooth_edges(Z: np.ndarray, border_size: int = 5) -> np.ndarray:
        """
        Smooth the edges of the height map to prevent sharp boundaries.

        Args:
            Z: Height array
            border_size: Size of border to smooth

        Returns:
            Smoothed height array
        """
        Z_smooth = Z.copy()
        
        for i in range(border_size):
            fade_factor = i / border_size
            # Top and bottom edges
            Z_smooth[i, :] = Z_smooth[i, :] * fade_factor
            Z_smooth[-(i+1), :] = Z_smooth[-(i+1), :] * fade_factor
            # Left and right edges
            Z_smooth[:, i] = Z_smooth[:, i] * fade_factor
            Z_smooth[:, -(i+1)] = Z_smooth[:, -(i+1)] * fade_factor
        
        return Z_smooth

    @staticmethod
    def generate_height_map_advanced(
        image_array: np.ndarray,
        max_height: float = 10.0,
        scale_xy: float = 100.0,
        resolution: float = 1.0,
        mode: str = "grayscale",
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate 3D height map from image using different modes.

        Args:
            image_array: Image array (0-1)
            max_height: Maximum height in mm
            scale_xy: XY scale factor
            resolution: Resolution factor (lower = more detailed)
            mode: Generation mode - "grayscale", "inverted", "edge_based", "color_to_height"

        Returns:
            Tuple of (X, Y, Z) mesh grids
        """
        if mode == "inverted":
            height_data = 1.0 - image_array
        elif mode == "edge_based":
            # Use edge detection for height
            from scipy import ndimage
            edges_x = ndimage.sobel(image_array, axis=0)
            edges_y = ndimage.sobel(image_array, axis=1)
            height_data = np.sqrt(edges_x**2 + edges_y**2)
            height_data = (height_data - height_data.min()) / (height_data.max() - height_data.min() + 1e-8)
        elif mode == "color_to_height":
            # Treat image as RGB and use maximum channel
            height_data = image_array
        else:  # grayscale (default)
            height_data = image_array
        
        # Apply resolution downsampling
        step = max(1, int(resolution))
        
        height, width = height_data.shape
        
        # Scale coordinates
        x = np.arange(0, width, step) * (scale_xy / width)
        y = np.arange(0, height, step) * (scale_xy / height)
        
        # Downsample image if needed
        if step > 1:
            z = height_data[::step, ::step]
        else:
            z = height_data
        
        # Create mesh grid
        X, Y = np.meshgrid(x, y)
        
        # Scale Z to height range
        Z = z * max_height
        
        return X, Y, Z
