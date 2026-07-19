"""Batch conversion of multiple images to STL files."""

import os
from pathlib import Path
from typing import Callable, Dict, Any

from .image_processor import ImageProcessor
from .height_map import HeightMapGenerator
from .stl_generator import STLGenerator


class BatchConverter:
    """Handle batch conversion of images to STL files."""

    @staticmethod
    def convert_directory(
        input_dir: str,
        output_dir: str,
        progress_callback: Callable[[int, int, str], None] = None,
        conversion_params: Dict[str, Any] = None,
    ) -> list[dict]:
        """
        Convert all images in a directory to STL files.

        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            progress_callback: Function called with (current, total, filename)
            conversion_params: Dictionary with conversion parameters

        Returns:
            List of results for each conversion
        """
        if conversion_params is None:
            conversion_params = {}

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Supported image formats
        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')
        
        # Find all images
        image_files = []
        for fmt in supported_formats:
            image_files.extend(Path(input_dir).glob(f'*{fmt}'))
            image_files.extend(Path(input_dir).glob(f'*{fmt.upper()}'))

        image_files = sorted(list(set(image_files)))  # Remove duplicates and sort

        results = []
        total = len(image_files)

        for idx, image_path in enumerate(image_files):
            if progress_callback:
                progress_callback(idx + 1, total, image_path.name)

            try:
                result = BatchConverter._convert_single(
                    str(image_path),
                    output_dir,
                    conversion_params,
                )
                result['status'] = 'success'
                results.append(result)
            except Exception as e:
                results.append({
                    'status': 'error',
                    'input': str(image_path),
                    'output': None,
                    'error': str(e),
                })

        return results

    @staticmethod
    def _convert_single(
        input_path: str,
        output_dir: str,
        params: Dict[str, Any],
    ) -> dict:
        """
        Convert a single image to STL.

        Args:
            input_path: Input image path
            output_dir: Output directory
            params: Conversion parameters

        Returns:
            Result dictionary
        """
        input_name = Path(input_path).stem
        output_path = str(Path(output_dir) / f"{input_name}.stl")

        # Get parameters with defaults
        scale = params.get('scale', 100)
        height = params.get('height', 10)
        resolution = params.get('resolution', 1.0)
        smooth = params.get('smooth', 1.0)
        mode = params.get('mode', 'grayscale')
        base = params.get('base', 2.0)
        invert = params.get('invert', False)
        contrast = params.get('contrast', 1.0)
        brightness = params.get('brightness', 1.0)

        # Load and process image
        image = ImageProcessor.load_image(input_path)
        image = ImageProcessor.resize_image(image, max_dimension=512)
        
        if contrast != 1.0:
            image = ImageProcessor.adjust_contrast(image, contrast)
        
        if brightness != 1.0:
            image = ImageProcessor.adjust_brightness(image, brightness)
        
        image = ImageProcessor.normalize_image(image)

        if smooth > 0:
            image = ImageProcessor.apply_smoothing(image, sigma=smooth)

        if invert:
            image = ImageProcessor.invert_image(image)

        # Generate height map
        X, Y, Z = HeightMapGenerator.generate_height_map_advanced(
            image,
            max_height=height,
            scale_xy=scale,
            resolution=resolution,
            mode=mode,
        )

        # Add base thickness
        Z = HeightMapGenerator.apply_base_thickness(Z, base_thickness=base)

        # Create mesh
        mesh = STLGenerator.create_mesh_from_height_map(X, Y, Z)
        
        # Make watertight
        mesh = STLGenerator.make_watertight(mesh)

        # Add base
        mesh = STLGenerator.add_base_to_mesh(mesh, base_height=base)

        # Save
        STLGenerator.save_stl(mesh, output_path)

        # Get mesh info
        info = STLGenerator.get_mesh_info(mesh)

        return {
            'input': input_path,
            'output': output_path,
            'vertices': info['vertices'],
            'faces': info['faces'],
            'volume': info['volume'],
            'watertight': info['is_watertight'],
        }
