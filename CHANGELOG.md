# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-19

### Added
- **GUI Interface** - Full Tkinter-based graphical user interface
  - Single image conversion with parameter sliders
  - Batch processing for multiple images
  - Help and settings tab with documentation
  - Real-time status display
  - Multi-threaded processing (non-blocking UI)

- **CLI Interface** - Command-line tools with Click
  - Single image conversion command
  - Batch conversion command
  - Preview generation command
  - 11 customizable parameters

- **Image Preprocessing**
  - Contrast adjustment (0.5-2.0)
  - Brightness control (0.5-2.0)
  - Gaussian smoothing
  - Edge detection (Sobel, Laplace, Canny)
  - Histogram equalization

- **Height Map Modes**
  - Grayscale (standard brightness-to-height)
  - Inverted (dark areas become tall)
  - Edge-based (emphasizes features)
  - Color-to-height (color intensity mapping)

- **Batch Processing**
  - Convert entire directories
  - Progress tracking
  - Error handling and reporting
  - Apply consistent settings

- **Mesh Optimization**
  - Automatic watertight mesh generation
  - Hole filling
  - Duplicate vertex merging
  - Normal orientation fixing

- **Preview Generation**
  - Height map heatmaps (PNG)
  - 3D model previews from multiple angles
  - Side-by-side comparisons
  - ASCII text previews

- **Documentation**
  - Comprehensive README
  - GUI user guide
  - Quick start guide
  - Feature descriptions
  - Visual guides and walkthroughs

### Technical Details
- **Python 3.8+** compatible
- **Cross-platform** (Windows, macOS, Linux)
- **No GUI dependencies** - Uses built-in Tkinter
- **Efficient processing** - NumPy/SciPy optimization
- **Professional output** - Trimesh 3D generation

### File Structure
```
Image2STL/
├── gui.py              # GUI launcher
├── src/
│   ├── cli/            # Command-line interface
│   ├── gui/            # GUI application
│   └── services/       # Core services (5 modules)
├── requirements.txt
├── setup.py
└── Documentation files
```

### Dependencies
- Pillow 10.1.0 - Image processing
- NumPy 1.26.2 - Array operations
- SciPy 1.11.4 - Scientific computing
- Trimesh 4.0.0 - 3D mesh generation
- Click 8.1.7 - CLI framework
- Matplotlib 3.8.2 - Visualization
- NetworkX 3.6.1 - Graph operations

## Future Enhancements

Planned features for future versions:

- [ ] Web interface
- [ ] Real-time 3D preview
- [ ] Advanced mesh editing
- [ ] Material properties
- [ ] Support for other 3D formats (OBJ, STL binary, etc.)
- [ ] Machine learning for automatic parameter suggestions
- [ ] Cloud processing for large images
- [ ] API server mode

## Version History

- **1.0.0** (2026-07-19) - Initial release with full feature set
