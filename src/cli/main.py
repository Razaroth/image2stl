"""Command-line interface for image2stl converter."""

import sys
import os
from pathlib import Path

import click

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.image_processor import ImageProcessor
from services.height_map import HeightMapGenerator
from services.stl_generator import STLGenerator
from services.batch_converter import BatchConverter
from services.preview import PreviewGenerator


@click.group()
def cli():
    """Image2STL - Convert images to 3D STL files."""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option(
    "--scale",
    default=100,
    type=float,
    help="XY scale factor (default: 100)",
)
@click.option(
    "--height",
    default=10,
    type=float,
    help="Maximum Z height in mm (default: 10)",
)
@click.option(
    "--resolution",
    default=1.0,
    type=float,
    help="Mesh resolution, lower = more detailed (default: 1.0)",
)
@click.option(
    "--mode",
    default="grayscale",
    type=click.Choice(["grayscale", "inverted", "edge_based", "color_to_height"]),
    help="Height map generation mode (default: grayscale)",
)
@click.option(
    "--base",
    default=2.0,
    type=float,
    help="Base thickness in mm (default: 2.0)",
)
@click.option(
    "--smooth",
    default=1.0,
    type=float,
    help="Smoothing factor (default: 1.0, 0 = no smoothing)",
)
@click.option(
    "--contrast",
    default=1.0,
    type=float,
    help="Contrast adjustment (default: 1.0)",
)
@click.option(
    "--brightness",
    default=1.0,
    type=float,
    help="Brightness adjustment (default: 1.0)",
)
@click.option(
    "--invert",
    is_flag=True,
    help="Invert the height map",
)
@click.option(
    "--max-dimension",
    default=512,
    type=int,
    help="Maximum image dimension (default: 512)",
)
@click.option(
    "--preview",
    is_flag=True,
    help="Generate preview images",
)
def convert(
    input_file: str,
    output_file: str,
    scale: float,
    height: float,
    resolution: float,
    mode: str,
    base: float,
    smooth: float,
    contrast: float,
    brightness: float,
    invert: bool,
    max_dimension: int,
    preview: bool,
):
    """Convert a single image to STL file."""
    
    try:
        click.echo(f"Loading image: {input_file}")
        
        # Load and process image
        image = ImageProcessor.load_image(input_file)
        original_image = image.copy()
        image = ImageProcessor.resize_image(image, max_dimension)
        
        if contrast != 1.0:
            click.echo(f"Adjusting contrast ({contrast})...")
            image = ImageProcessor.adjust_contrast(image, contrast)
        
        if brightness != 1.0:
            click.echo(f"Adjusting brightness ({brightness})...")
            image = ImageProcessor.adjust_brightness(image, brightness)
        
        image = ImageProcessor.normalize_image(image)

        if smooth > 0:
            click.echo(f"Applying smoothing (sigma={smooth})...")
            image = ImageProcessor.apply_smoothing(image, sigma=smooth)

        if invert:
            click.echo("Inverting height map...")
            image = ImageProcessor.invert_image(image)

        click.echo(f"Generating height map ({mode} mode)...")
        X, Y, Z = HeightMapGenerator.generate_height_map_advanced(
            image,
            max_height=height,
            scale_xy=scale,
            resolution=resolution,
            mode=mode,
        )

        click.echo("Adding base thickness...")
        Z = HeightMapGenerator.apply_base_thickness(Z, base_thickness=base)

        click.echo("Creating 3D mesh...")
        mesh = STLGenerator.create_mesh_from_height_map(X, Y, Z)
        
        click.echo("Making mesh watertight...")
        mesh = STLGenerator.make_watertight(mesh)

        click.echo("Adding base...")
        mesh = STLGenerator.add_base_to_mesh(mesh, base_height=base)

        # Get mesh info
        info = STLGenerator.get_mesh_info(mesh)

        click.echo("Saving STL file...")
        STLGenerator.save_stl(mesh, output_file)

        # Generate previews if requested
        if preview:
            output_dir = Path(output_file).parent
            base_name = Path(output_file).stem
            
            click.echo("Generating preview images...")
            
            # Height map preview
            height_preview = output_dir / f"{base_name}_height_map.png"
            PreviewGenerator.generate_height_map_preview(Z, str(height_preview))
            click.echo(f"  Height map: {height_preview}")
            
            # Comparison preview
            comparison_preview = output_dir / f"{base_name}_comparison.png"
            PreviewGenerator.generate_comparison_preview(original_image, image, str(comparison_preview))
            click.echo(f"  Comparison: {comparison_preview}")
            
            # 3D preview
            try:
                preview_3d = output_dir / f"{base_name}_3d_preview.png"
                PreviewGenerator.generate_3d_preview(mesh, str(preview_3d))
                click.echo(f"  3D model: {preview_3d}")
            except Exception as e:
                click.echo(f"  Warning: 3D preview failed - {e}")

        click.echo("\n✓ Conversion successful!")
        click.echo(f"Output file: {output_file}")
        click.echo(f"Vertices: {info['vertices']}")
        click.echo(f"Faces: {info['faces']}")
        click.echo(f"Volume: {info['volume']:.2f} mm³")
        click.echo(f"Watertight: {info['is_watertight']}")
        
    except FileNotFoundError as e:
        click.echo(f"Error: Input file not found - {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("input_dir", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path())
@click.option("--scale", default=100, type=float, help="XY scale factor")
@click.option("--height", default=10, type=float, help="Maximum Z height")
@click.option("--resolution", default=1.0, type=float, help="Mesh resolution")
@click.option("--mode", default="grayscale", type=click.Choice(["grayscale", "inverted", "edge_based", "color_to_height"]))
@click.option("--base", default=2.0, type=float, help="Base thickness")
@click.option("--smooth", default=1.0, type=float, help="Smoothing factor")
@click.option("--contrast", default=1.0, type=float, help="Contrast adjustment")
@click.option("--brightness", default=1.0, type=float, help="Brightness adjustment")
def batch(
    input_dir: str,
    output_dir: str,
    scale: float,
    height: float,
    resolution: float,
    mode: str,
    base: float,
    smooth: float,
    contrast: float,
    brightness: float,
):
    """Convert all images in a directory to STL files."""
    
    try:
        click.echo(f"Starting batch conversion: {input_dir} -> {output_dir}")
        
        conversion_params = {
            'scale': scale,
            'height': height,
            'resolution': resolution,
            'mode': mode,
            'base': base,
            'smooth': smooth,
            'contrast': contrast,
            'brightness': brightness,
        }

        def progress(current, total, filename):
            click.echo(f"  [{current}/{total}] {filename}...", nl=False)

        results = BatchConverter.convert_directory(
            input_dir,
            output_dir,
            progress_callback=progress,
            conversion_params=conversion_params,
        )

        # Print results
        click.echo("\n\nBatch Conversion Results:")
        click.echo("=" * 60)
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = len(results) - success_count
        
        click.echo(f"Total: {len(results)} | Success: {success_count} | Errors: {error_count}")
        
        for result in results:
            if result['status'] == 'success':
                click.echo(f"\n✓ {Path(result['input']).name}")
                click.echo(f"  Output: {result['output']}")
                click.echo(f"  Vertices: {result['vertices']} | Faces: {result['faces']}")
                click.echo(f"  Watertight: {result['watertight']}")
            else:
                click.echo(f"\n✗ {Path(result.get('input', 'Unknown')).name}")
                click.echo(f"  Error: {result['error']}")
                
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path())
@click.option("--format", default="png", type=click.Choice(["png", "ascii"]), help="Preview format")
def preview(input_file: str, output_dir: str, format: str):
    """Generate previews for an image."""
    
    try:
        click.echo(f"Loading image: {input_file}")
        
        # Load image
        image = ImageProcessor.load_image(input_file)
        image = ImageProcessor.normalize_image(image)
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        base_name = Path(input_file).stem
        
        if format == "png":
            click.echo("Generating preview images...")
            
            # Generate height map visualization
            # Create a simple height map for preview
            Z = image * 10  # Simple height map
            
            preview_path = Path(output_dir) / f"{base_name}_preview.png"
            PreviewGenerator.generate_height_map_preview(Z, str(preview_path))
            click.echo(f"✓ Preview saved: {preview_path}")
        
        elif format == "ascii":
            ascii_path = Path(output_dir) / f"{base_name}_ascii.txt"
            PreviewGenerator.generate_quick_preview(image, str(ascii_path))
            click.echo(f"✓ ASCII preview saved: {ascii_path}")
            
            # Display ASCII art
            with open(ascii_path) as f:
                click.echo("\n" + f.read())
                
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
