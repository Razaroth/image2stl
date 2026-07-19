# Image2STL - Quick Start Guide

## 🚀 Quick Commands

### Single Image
```bash
# Basic conversion
python -m src.cli.main convert image.png model.stl

# With all features
python -m src.cli.main convert photo.jpg model.stl \
  --mode edge_based \
  --contrast 1.5 \
  --brightness 1.1 \
  --smooth 2.0 \
  --height 20 \
  --scale 150 \
  --resolution 0.5 \
  --preview
```

### Batch Conversion
```bash
# Convert entire folder
python -m src.cli.main batch images/ output/ --height 15 --contrast 1.5
```

### Preview
```bash
# Visual preview (PNG)
python -m src.cli.main preview image.png output/ --format png

# Text preview (ASCII art)
python -m src.cli.main preview image.png output/ --format ascii
```

---

## 📊 Height Map Modes

| Mode | Best For | Example |
|------|----------|---------|
| **grayscale** | Most images | Photos, general art |
| **inverted** | Dark themes | Inverted designs |
| **edge_based** | Maps, logos | Road maps, outlines |
| **color_to_height** | Color-coded data | Heatmaps, color gradients |

---

## 🎨 Image Enhancement Options

| Option | Range | Effect |
|--------|-------|--------|
| `--contrast` | 0.5-2.0 | Enhance or soften details |
| `--brightness` | 0.5-2.0 | Lighten or darken |
| `--smooth` | 0-5 | Reduce noise (higher = smoother) |

---

## 📁 Generated Files

With `--preview`, you get:
- ✓ `model.stl` - 3D model for printing
- ✓ `model_height_map.png` - Color visualization
- ✓ `model_comparison.png` - Original vs height map
- ✓ `model_3d_preview.png` - 3D views from 4 angles

---

## 🔧 All Options Reference

```
COMMON OPTIONS:
  --scale N              XY size (default: 100)
  --height N             Max height in mm (default: 10)
  --resolution N         Detail level (default: 1.0)
  --base N               Base thickness mm (default: 2.0)

IMAGE ENHANCEMENT:
  --contrast N           Enhance details (1.0 = no change)
  --brightness N         Adjust brightness
  --smooth N             Gaussian blur factor

HEIGHT MAP:
  --mode TYPE            grayscale | inverted | edge_based | color_to_height
  --invert               Flip height values

OUTPUT:
  --preview              Generate preview images
  --max-dimension N      Max image size (default: 512)
```

---

## ✨ New Features Summary

### 1. **Watertight Meshes** ✓
Automatic hole-filling and normal fixing for reliable 3D printing.

### 2. **Image Preprocessing** ✓
- Contrast adjustment
- Brightness control
- Edge detection (Sobel, Laplace, Canny)
- Histogram equalization

### 3. **Multiple Height Map Modes** ✓
- Grayscale (default)
- Inverted
- Edge-based (emphasizes features)
- Color-to-height

### 4. **Batch Processing** ✓
Convert entire directories with progress tracking and error reporting.

### 5. **Visual Previews** ✓
- Height map heatmaps
- Side-by-side comparisons
- 3D model from multiple angles
- ASCII text previews

---

## 📚 More Information

- **Full documentation:** See `README.md`
- **Feature details:** See `FEATURES.md`
- **Run demo:** `python demo.py`

---

## 💡 Tips & Tricks

### For 3D Printing
```bash
# Good defaults for printing
python -m src.cli.main convert design.png model.stl \
  --height 15 \
  --base 3 \
  --smooth 1.5
```

### For Fine Details
```bash
# Preserve details
python -m src.cli.main convert image.png model.stl \
  --resolution 0.5 \
  --contrast 1.5 \
  --smooth 0.5
```

### For Smooth Models
```bash
# High smoothing
python -m src.cli.main convert photo.jpg model.stl \
  --smooth 3.0 \
  --base 2
```

### Preview Before Print
```bash
# Check ASCII preview first
python -m src.cli.main preview image.png output/ --format ascii

# Then convert if satisfied
python -m src.cli.main convert image.png final.stl --height 20
```

---

## 📞 Troubleshooting

**Issue:** Non-watertight mesh → **Solution:** Already automatic! Uses hole-filling algorithm.

**Issue:** Too much detail noise → **Solution:** Increase `--smooth` (try 2.0-3.0)

**Issue:** Lost details → **Solution:** Decrease `--smooth` (try 0.5) and increase `--contrast` (try 1.5-2.0)

**Issue:** Model too thin → **Solution:** Increase `--base` (try 3-5mm) or `--height` (try 20-30)

---

## 🎯 Use Cases

| Use Case | Command |
|----------|---------|
| Photo to model | `convert photo.jpg model.stl --height 15` |
| Logo/icon | `convert logo.png model.stl --mode edge_based --contrast 2` |
| Terrain map | `convert map.png terrain.stl --scale 200 --mode edge_based` |
| Low-poly art | `convert art.png model.stl --resolution 2 --smooth 2` |
| High-detail | `convert detail.png model.stl --resolution 0.5 --smooth 0.5` |
| Batch job | `batch images/ output/ --height 12 --contrast 1.2` |

---

Generated with ❤️ for 3D printing enthusiasts!
