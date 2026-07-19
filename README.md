# Image2STL - Convert Images to 3D STL Files

A powerful and easy-to-use tool to convert 2D images into 3D STL files suitable for 3D printing.

## 🚀 Quick Start

### **GUI Mode (Easiest)** ✨

```bash
python gui.py
```

A user-friendly graphical interface with:
- Intuitive file selection
- Live parameter sliders
- Batch conversion support
- Real-time progress updates
- Built-in preview generation

**[See GUI Guide →](GUI_GUIDE.md)**

### **Command Line Mode**

```bash
# Single image conversion
python -m src.cli.main convert image.png model.stl

# Batch conversion
python -m src.cli.main batch images/ output/

# Generate previews
python -m src.cli.main preview image.png output/
```

## Features

- **GUI or CLI** - Choose your preference
- **Simple & Powerful** - Easy for beginners, advanced for experts
- **Height map generation** - Multiple mapping modes
- **Batch processing** - Convert entire directories
- **Preprocessing** - Contrast, brightness, smoothing controls
- **Watertight meshes** - Optimized for 3D printing
- **Preview generation** - Visualize before printing
- **Multiple modes** - Grayscale, edge-based, inverted, color-to-height

## Installation

```bash
pip install -r requirements.txt
python setup.py install
```

Or for development:
```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### GUI Mode (Recommended for Most Users)

**Launch the graphical interface:**
```bash
python gui.py
```

- Browse files with buttons
- Adjust settings with sliders
- Real-time feedback and status
- No command-line needed

[Detailed GUI Guide →](GUI_GUIDE.md)

### Command Line Mode (Advanced)

### Single Image Conversion

```bash
python -m src.cli.main convert input.png output.stl [OPTIONS]
```

**Options:**
- `--scale` - XY scale factor (default: 100)
- `--height` - Maximum Z height in mm (default: 10)
- `--resolution` - Mesh resolution, lower = more detailed (default: 1.0)
- `--mode` - Height map mode: grayscale|inverted|edge_based|color_to_height (default: grayscale)
- `--base` - Base thickness in mm (default: 2.0)
- `--smooth` - Smoothing factor (default: 1.0, 0 = no smoothing)
- `--contrast` - Contrast adjustment (default: 1.0)
- `--brightness` - Brightness adjustment (default: 1.0)
- `--invert` - Invert the height map (flag)
- `--preview` - Generate preview images (flag)

### Batch Conversion

Convert all images in a directory:

```bash
python -m src.cli.main batch input_dir/ output_dir/ [OPTIONS]
```

Supports all the same options as single conversion, applies to all images.

### Preview Generation

Generate previews without creating STL:

```bash
python -m src.cli.main preview input.png output_dir/ --format png
```

Formats: `png` (visual) or `ascii` (text-based)

## Examples

### Basic Conversion
```bash
python -m src.cli.main convert photo.jpg model.stl
```

### High Detail Model
```bash
python -m src.cli.main convert artwork.png artwork_3d.stl --scale 150 --height 20 --resolution 0.5
```

### Edge-Based Model (Emphasize Features)
```bash
python -m src.cli.main convert photo.jpg edges.stl --mode edge_based --height 15
```

### Batch Conversion with Custom Settings
```bash
python -m src.cli.main batch images/ stl_output/ --height 25 --contrast 1.5 --smooth 2.0
```

### Generate Previews with Original Image
```bash
python -m src.cli.main convert photo.jpg model.stl --preview
```

This creates:
- `model.stl` - Final 3D model
- `model_height_map.png` - Color-mapped height map
- `model_comparison.png` - Side-by-side original vs height map
- `model_3d_preview.png` - 3D model from multiple angles

## Height Map Modes

- **grayscale** - Standard: brightness = height
- **inverted** - Inverted: dark = high, bright = low
- **edge_based** - Emphasizes edges and features
- **color_to_height** - Uses color intensity as height

## Tips for Best Results

1. **Contrast adjustment** - Use `--contrast 1.5` to 2.0 for better details
2. **Smoothing** - Use `--smooth 2.0` for less noise, `--smooth 0.5` for sharp features
3. **Resolution** - Lower values (0.5-1.0) create more detail but larger files
4. **Base thickness** - Higher values (3-5mm) provide better structural support
5. **Test with preview** - Use `--preview` to verify before full conversion

## Architecture

- **ImageProcessor** - Image loading, preprocessing, normalization
- **HeightMapGenerator** - Height map generation with multiple modes
- **STLGenerator** - Mesh creation and STL export with watertight support
- **BatchConverter** - Batch processing with progress tracking
- **PreviewGenerator** - Visual previews (height maps, 3D, comparisons)
- **GUI App** - User-friendly graphical interface (Tkinter)

## Requirements

- Python 3.8+
- Pillow - Image processing
- NumPy/SciPy - Array operations
- Trimesh - 3D mesh generation
- Click - CLI framework
- Matplotlib - Preview generation
- Tkinter - GUI (usually included with Python)

