# Image2STL GUI - Easy User Interface

## 🎯 Quick Start

### Launch the GUI

```bash
python gui.py
```

Or double-click `gui.py` if you're on Windows.

---

## 📋 Tabs

### 1. **Single Image** Tab
Convert one image to STL with full control:

- **Input Image** - Browse and select your image file
- **Output STL** - Choose where to save the STL model
- **Settings** - Adjust all parameters with sliders
  - **Scale** - XY size (50-300)
  - **Height** - Maximum Z height in mm (5-50)
  - **Resolution** - Mesh detail level (0.5=detailed, 3.0=coarse)
  - **Smoothing** - Reduce noise (0=sharp, 5=very smooth)
  - **Contrast** - Enhance/reduce details (0.5-2.0)
  - **Brightness** - Lighten/darken (0.5-2.0)
  - **Base Thickness** - Bottom support (1-10 mm)
- **Height Map Mode** - Choose conversion method
  - Grayscale (standard)
  - Inverted (dark=high)
  - Edge-based (emphasize features)
  - Color-to-height (color intensity)
- **Checkboxes**
  - Invert Height Map
  - Generate Preview Images
- **Status** - Real-time progress and results

### 2. **Batch Convert** Tab
Convert entire folders with consistent settings:

- **Input Directory** - Select folder with images
- **Output Directory** - Where to save all STL files
- **Settings** - Applied to all images
  - Height
  - Contrast
  - Smoothing
- **Progress Bar** - Visual progress indicator
- **Status** - Results for each file

### 3. **Help & Settings** Tab
Reference guide with:
- Mode descriptions
- Parameter explanations
- Tips for best results
- Preview information

---

## 🎨 Features

✓ **Easy File Selection** - Browse buttons for all inputs
✓ **Live Parameter Preview** - See values update on sliders
✓ **Real-time Status** - Watch conversion progress
✓ **Error Handling** - Clear error messages if something fails
✓ **Multi-threaded** - GUI stays responsive during conversion
✓ **Batch Processing** - Convert multiple images at once
✓ **Auto Preview** - Optional preview image generation
✓ **Intuitive Design** - No command-line knowledge needed

---

## 💡 Workflow Examples

### Basic Image to STL
1. Click **"Single Image"** tab
2. Click **"Browse..."** next to Input Image
3. Select your image file
4. Click **"Browse..."** next to Output STL
5. Choose save location and name
6. Click **"Convert to STL"**
7. Wait for completion (check Status box)

### High-Quality Model with Preview
1. Select input and output files
2. Adjust sliders:
   - Contrast: 1.5 (more details)
   - Smoothing: 2.0 (less noise)
   - Height: 20 (taller)
3. Enable "Generate Preview Images"
4. Click "Convert to STL"
5. Review preview images in output folder

### Batch Convert Folder
1. Click **"Batch Convert"** tab
2. Browse to input folder (with multiple images)
3. Browse to output folder
4. Set Height and Contrast for all
5. Click **"Convert All"**
6. Watch progress bar fill
7. Check Status box for results

---

## ⚙️ Parameter Guide

| Parameter | Range | Effect | Best For |
|-----------|-------|--------|----------|
| Scale | 50-300 | Size of XY axes | Larger = bigger model |
| Height | 5-50 mm | Max Z height | 10-15 for most prints |
| Resolution | 0.5-3.0 | Mesh detail | 0.5-1.0 = very detailed |
| Smoothing | 0-5 | Noise reduction | 1.0-2.0 = balanced |
| Contrast | 0.5-2.0 | Detail emphasis | 1.5 = more details |
| Brightness | 0.5-2.0 | Image lightness | 1.0 = normal |
| Base Thickness | 1-10 mm | Bottom support | 2-3 mm = stable |

---

## 🖼️ Preview Images

When enabled, creates:
- **Height Map** - Color visualization of heights
- **Comparison** - Side-by-side original vs height map
- **3D Model** - 3D mesh from multiple viewing angles

Check these before 3D printing!

---

## 🎯 Tips for Best Results

✓ **Start with defaults** - They work for most images
✓ **Enable previews first** - Check before full conversion
✓ **Adjust contrast** - 1.5-2.0 for subtle details
✓ **Use smoothing** - 2.0 for smooth surfaces
✓ **Edge-based mode** - Great for maps and logos
✓ **Batch test** - Convert one image first with new settings

---

## 🐛 Troubleshooting

**GUI won't start?**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Try running from project directory: `cd Image2STL` then `python gui.py`

**Conversion is slow?**
- Reduce resolution value (0.5 = slower but more detail)
- Reduce image size
- Close other applications

**Model looks wrong?**
- Try different Height Map Mode (edge_based for outlines)
- Adjust Contrast up (more details)
- Reduce Smoothing (sharper features)

**Error during conversion?**
- Check input image format (PNG, JPG, BMP supported)
- Ensure output directory exists or is writable
- See Status box for specific error message

---

## 📂 File Structure

```
Image2STL/
├── gui.py                    ← Launch script
├── src/
│   └── gui/
│       ├── __init__.py
│       └── app.py            ← Main GUI application
└── ...
```

---

## 🚀 Next Steps

1. **Try Single Image** - Convert a test image
2. **Review Previews** - Check generated preview images
3. **Adjust Settings** - Fine-tune for your needs
4. **Batch Convert** - Process multiple images
5. **3D Print** - Use output STL with your slicer

---

## 💻 System Requirements

- Python 3.8+
- All packages from requirements.txt
- Tkinter (usually included with Python)

---

No command-line knowledge needed! 🎉
