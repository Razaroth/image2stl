# Image2STL

Convert 2D images to 3D STL files for 3D printing with ease!

## ✨ Features

- **GUI & CLI** - Choose your interface
- **4 Height Map Modes** - Grayscale, inverted, edge-based, color-to-height
- **Image Preprocessing** - Contrast, brightness, smoothing controls
- **Batch Processing** - Convert multiple images at once
- **Watertight Meshes** - Optimized for 3D printing
- **Preview Generation** - Visualize before printing

## 🚀 Quick Start

### GUI Mode (Easiest)
```bash
python gui.py
```

### CLI Mode
```bash
python -m src.cli.main convert image.png model.stl
python -m src.cli.main batch images/ output/
```

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 📖 Documentation

- [GUI Guide](GUI_GUIDE.md) - Complete GUI documentation
- [Quick Start](QUICKSTART.md) - Quick reference
- [Features](FEATURES.md) - Feature descriptions
- [README](README.md) - Full documentation

## 📂 Project Structure

```
Image2STL/
├── gui.py                 # Launch GUI
├── src/
│   ├── cli/              # Command-line interface
│   ├── gui/              # Graphical interface
│   └── services/         # Core conversion services
├── test_images/          # Sample images
├── output/               # Generated models
└── docs/                 # Documentation
```

## 🎯 Usage Examples

### Basic Conversion
```bash
python gui.py
# Or
python -m src.cli.main convert photo.jpg model.stl
```

### Advanced Options
```bash
python -m src.cli.main convert image.png model.stl \
  --mode edge_based --contrast 1.5 --height 20 --preview
```

### Batch Conversion
```bash
python -m src.cli.main batch images/ output/ --height 15 --contrast 1.2
```

## 💡 Tips

- Start with GUI for interactive use
- Use CLI for automation and scripting
- Enable previews to check quality
- Try different modes for different results
- Adjust contrast/smoothing for fine-tuning

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report issues
- Suggest features
- Submit pull requests

## 📄 License

MIT License - see LICENSE file

## 🙏 Credits

Built with:
- Python 3.8+
- Pillow, NumPy, SciPy
- Trimesh for 3D mesh generation
- Click for CLI
- Tkinter for GUI
