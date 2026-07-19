"""Preview generation for height maps and 3D models."""

import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class PreviewGenerator:
    """Generate previews of height maps and 3D models."""

    @staticmethod
    def generate_height_map_preview(
        Z: np.ndarray,
        output_path: str,
        colormap: str = "viridis",
    ) -> None:
        """
        Generate a preview image of the height map with color mapping.

        Args:
            Z: Height array
            output_path: Path to save the preview
            colormap: Matplotlib colormap name (e.g., 'viridis', 'hot', 'cool')
        """
        # Normalize Z to 0-1
        Z_norm = (Z - Z.min()) / (Z.max() - Z.min() + 1e-8)

        # Create figure
        plt.figure(figsize=(10, 8), dpi=100)
        
        # Create heatmap
        im = plt.imshow(Z_norm, cmap=colormap, origin='lower')
        
        # Add colorbar
        cbar = plt.colorbar(im, label='Height (normalized)')
        
        # Labels
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Height Map Preview')
        
        # Save
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()

    @staticmethod
    def generate_3d_preview(
        mesh,
        output_path: str,
        views: list[tuple[int, int]] = None,
    ) -> None:
        """
        Generate a 2D preview of the 3D mesh from multiple angles.

        Args:
            mesh: Trimesh object
            output_path: Path to save the preview
            views: List of (elevation, azimuth) angles for different views
        """
        if views is None:
            views = [(20, 45), (20, 135), (20, 225), (20, 315)]

        try:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
        except ImportError:
            raise ImportError("matplotlib is required for 3D preview generation")

        # Create subplots for different views
        num_views = len(views)
        fig = plt.figure(figsize=(12, 3 * ((num_views + 1) // 2)))

        for idx, (elev, azim) in enumerate(views, 1):
            ax = fig.add_subplot(2, 2, idx, projection='3d')

            # Plot mesh
            ax.plot_trisurf(
                mesh.vertices[:, 0],
                mesh.vertices[:, 1],
                mesh.vertices[:, 2],
                triangles=mesh.faces,
                alpha=0.8,
                edgecolor='gray',
                linewidth=0.1,
            )

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.view_init(elev=elev, azim=azim)
            ax.set_title(f'View: {elev}° elevation, {azim}° azimuth')

        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()

    @staticmethod
    def generate_comparison_preview(
        original_image: np.ndarray,
        height_map: np.ndarray,
        output_path: str,
    ) -> None:
        """
        Generate a side-by-side comparison of original image and height map.

        Args:
            original_image: Original grayscale image (0-255)
            height_map: Generated height map (0-1)
            output_path: Path to save the preview
        """
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Original image
        axes[0].imshow(original_image, cmap='gray')
        axes[0].set_title('Original Image')
        axes[0].axis('off')

        # Height map
        im = axes[1].imshow(height_map, cmap='viridis')
        axes[1].set_title('Height Map')
        axes[1].axis('off')
        plt.colorbar(im, ax=axes[1], label='Height')

        plt.tight_layout()
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()

    @staticmethod
    def generate_quick_preview(
        height_map: np.ndarray,
        output_path: str,
    ) -> None:
        """
        Generate a quick text-based ASCII preview of the height map.

        Args:
            height_map: Height array (0-1)
            output_path: Path to save the preview
        """
        # Normalize
        normalized = (height_map - height_map.min()) / (height_map.max() - height_map.min() + 1e-8)

        # Sample down for ASCII art
        sample_height = min(20, normalized.shape[0])
        sample_width = min(80, normalized.shape[1])

        y_indices = np.linspace(0, normalized.shape[0] - 1, sample_height, dtype=int)
        x_indices = np.linspace(0, normalized.shape[1] - 1, sample_width, dtype=int)

        sampled = normalized[np.ix_(y_indices, x_indices)]

        # ASCII characters by brightness
        chars = ' .:-=+*#%@'

        with open(output_path, 'w') as f:
            f.write("Height Map Preview (ASCII Art)\n")
            f.write("=" * sample_width + "\n")
            for row in sampled:
                line = ''.join(chars[int(val * (len(chars) - 1))] for val in row)
                f.write(line + '\n')
            f.write("=" * sample_width + "\n")
