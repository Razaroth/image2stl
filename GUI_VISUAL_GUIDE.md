# 🎨 Image2STL GUI - Visual Overview

## Application Window

```
╔════════════════════════════════════════════════════════════════╗
║  Image2STL Converter                                    [_][□][X]║
╠════════════════════════════════════════════════════════════════╣
║ ┌─ Single Image ─┐ ┌─ Batch Convert ─┐ ┌─ Help & Settings ─┐ ║
║ │ ┌──────────────────────────────────────────────────────────┐│ ║
║ │ │ Convert Single Image                                    ││ ║
║ │ │                                                          ││ ║
║ │ │ Input Image                                             ││ ║
║ │ │ [________________________] [Browse...]                  ││ ║
║ │ │                                                          ││ ║
║ │ │ Output STL File                                         ││ ║
║ │ │ [________________________] [Browse...]                  ││ ║
║ │ │                                                          ││ ║
║ │ │ ┌─ Settings ────────────────────────────────────────┐  ││ ║
║ │ │ │ Scale (XY):                 ●─────────── 100    │  ││ ║
║ │ │ │ Height (mm):                ●─────────── 10     │  ││ ║
║ │ │ │ Resolution:                 ●─────────── 1.0    │  ││ ║
║ │ │ │ Smoothing:                  ●─────────── 1.0    │  ││ ║
║ │ │ │ Contrast:                   ●─────────── 1.0    │  ││ ║
║ │ │ │ Brightness:                 ●─────────── 1.0    │  ││ ║
║ │ │ │ Base Thickness (mm):        ●─────────── 2.0    │  ││ ║
║ │ │ │                                                │  ││ ║
║ │ │ │ Height Map Mode:        [▼ grayscale      ]    │  ││ ║
║ │ │ │                                                │  ││ ║
║ │ │ │ ☐ Invert Height Map                           │  ││ ║
║ │ │ │ ☑ Generate Preview Images                      │  ││ ║
║ │ │ └────────────────────────────────────────────────┘  ││ ║
║ │ │                                                      ││ ║
║ │ │ [════════ Convert to STL ════════]                   ││ ║
║ │ │                                                      ││ ║
║ │ │ ┌─ Status ─────────────────────────────────────────┐ ││ ║
║ │ │ │ Loading image...                                │ ││ ║
║ │ │ │ Adjusting contrast (1.5)...                     │ ││ ║
║ │ │ │ Smoothing (sigma=2.0)...                        │ ││ ║
║ │ │ │ Generating height map (grayscale mode)...      │ ││ ║
║ │ │ │ Creating 3D mesh...                            │ ││ ║
║ │ │ │ ✓ Conversion Successful!                       │ ││ ║
║ │ │ │ Vertices: 65544 | Faces: 130062                │ ││ ║
║ │ │ └────────────────────────────────────────────────┘ ││ ║
║ │ └──────────────────────────────────────────────────────┘│ ║
║ └──────────────────────────────────────────────────────────┘ ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Batch Convert Tab

```
╔════════════════════════════════════════════════════════════════╗
║              Batch Convert Images                              ║
║                                                                ║
║ Input Directory                                               ║
║ [________________________] [Browse...]                        ║
║                                                                ║
║ Output Directory                                              ║
║ [________________________] [Browse...]                        ║
║                                                                ║
║ Settings (Applied to All)                                     ║
║ ┌──────────────────────────────────────────────────────────┐  ║
║ │ Height (mm):          ●─────────── 10                   │  ║
║ │ Contrast:            ●─────────── 1.0                  │  ║
║ │ Smoothing:           ●─────────── 1.0                  │  ║
║ └──────────────────────────────────────────────────────────┘  ║
║                                                                ║
║ [══════════════ Convert All ══════════════]                    ║
║                                                                ║
║ [████████████████████░░░░░░░░░░░░░░░░] 60%                   ║
║                                                                ║
║ Status                                                         ║
║ ┌──────────────────────────────────────────────────────────┐  ║
║ │ [1/4] image1.jpg...                                     │  ║
║ │ [2/4] image2.png...                                     │  ║
║ │ [3/4] logo.jpg...                                       │  ║
║ │ ✓ image1.jpg                                           │  ║
║ │   Vertices: 65544 | Faces: 130062 | Watertight: True  │  ║
║ │                                                         │  ║
║ │ Results: Success: 3, Errors: 0                        │  ║
║ └──────────────────────────────────────────────────────────┘  ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Features Visualization

### Single Image Tab
```
┌─────────────────────────────────────────┐
│ INPUT SELECTION                         │
├─────────────────────────────────────────┤
│ Browse Image File                       │
│ ↓ Select PNG, JPG, BMP, etc.           │
│ /path/to/image.jpg                      │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ PARAMETER ADJUSTMENT                    │
├─────────────────────────────────────────┤
│ [Slider]  Scale                         │
│ [Slider]  Height                        │
│ [Slider]  Smoothing                     │
│ [Dropdown] Mode Selection               │
│ [Checkbox] Invert / Preview             │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ CONVERSION PROCESS                      │
├─────────────────────────────────────────┤
│ 1. Load image                           │
│ 2. Preprocess (contrast, brightness)    │
│ 3. Generate height map                  │
│ 4. Create 3D mesh                       │
│ 5. Make watertight                      │
│ 6. Export to STL                        │
│ 7. Generate previews (optional)         │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ OUTPUT                                  │
├─────────────────────────────────────────┤
│ ✓ model.stl          (6.5 MB)           │
│ ✓ model_height_map.png  (visible)       │
│ ✓ model_comparison.png  (visible)       │
│ ✓ model_3d_preview.png  (visible)       │
└─────────────────────────────────────────┘
```

### Batch Tab
```
┌──────────────────────────────────────────┐
│ INPUT FOLDER SELECTION                  │
├──────────────────────────────────────────┤
│ Select folder with multiple images      │
│ images/                                  │
│   ├─ photo1.jpg                         │
│   ├─ photo2.jpg                         │
│   ├─ logo.png                           │
│   └─ design.bmp                         │
└──────────────────────────────────────────┘
         ↓
┌──────────────────────────────────────────┐
│ BATCH SETTINGS                          │
├──────────────────────────────────────────┤
│ Apply same settings to all:             │
│ • Height: 12 mm                         │
│ • Contrast: 1.2                         │
│ • Smoothing: 1.5                        │
└──────────────────────────────────────────┘
         ↓
┌──────────────────────────────────────────┐
│ PROGRESS TRACKING                       │
├──────────────────────────────────────────┤
│ [████████████░░░░░░░░] 60% (3/5)        │
│ Currently processing: logo.png...       │
└──────────────────────────────────────────┘
         ↓
┌──────────────────────────────────────────┐
│ RESULTS                                 │
├──────────────────────────────────────────┤
│ ✓ photo1.jpg → photo1.stl               │
│ ✓ photo2.jpg → photo2.stl               │
│ ✓ logo.png → logo.stl                   │
│ ✓ design.bmp → design.stl               │
│ ✗ broken.jpg → ERROR: Invalid format    │
│                                         │
│ Summary: Success 4/5, Errors: 1         │
└──────────────────────────────────────────┘
```

---

## User Workflow

```
START
  │
  ├─→ CLICK "gui.py" or "python gui.py"
  │
  ├─→ CHOOSE MODE
  │   ├─ Single Image  (for one file)
  │   └─ Batch        (for multiple)
  │
  ├─→ SELECT FILES/FOLDERS
  │   ├─ Browse buttons for easy selection
  │   └─ Auto-population of output path
  │
  ├─→ ADJUST SLIDERS
  │   ├─ Real-time value display
  │   ├─ Preset combinations for common uses
  │   └─ Help tab for reference
  │
  ├─→ ENABLE OPTIONS
  │   ├─ ☑ Generate Preview
  │   ├─ ☐ Invert Height Map
  │   └─ Choose Height Map Mode
  │
  ├─→ CLICK "CONVERT"
  │   ├─ Status updates in real-time
  │   ├─ Progress bar (batch mode)
  │   └─ GUI stays responsive
  │
  ├─→ REVIEW RESULTS
  │   ├─ Check status box for details
  │   ├─ View preview images (if enabled)
  │   └─ Success/error message dialog
  │
  ├─→ FIND OUTPUT
  │   ├─ STL file ready for 3D printing
  │   ├─ Preview images in same folder
  │   └─ Can open in 3D slicer software
  │
  └─→ END
```

---

## Parameter Slider Guide

### Scale Slider
```
        Low              Medium              High
    Small model ────→ Normal ────→ Large model
        50            100             300
```

### Height Slider  
```
        Short           Medium           Tall
    Flat model ────→ Balanced ────→ Dramatic height
        5 mm           10 mm           50 mm
```

### Smoothing Slider
```
      Sharp              Balanced           Smooth
   Fine details ────→ Mix of both ────→ Very smooth
        0                1.0               5.0
```

### Contrast Slider
```
      Subtle             Normal            Enhanced
   Less detail ────→ Standard ────→ More details
        0.5               1.0              2.0
```

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Convert | Ctrl+Enter (when ready) |
| Clear Status | Ctrl+L (in status box) |
| Browse Input | Alt+I |
| Browse Output | Alt+O |

---

## Color Scheme

- **Background**: Light gray
- **Controls**: Standard Windows/OS theme
- **Status Text**: Black on white
- **Success Messages**: Green checkmarks ✓
- **Error Messages**: Red X marks ✗
- **Progress Bar**: Blue fill

---

## Responsiveness

- **Conversions run in background threads** - GUI never freezes
- **Real-time status updates** - See progress as it happens
- **Cancel button available** - Stop long-running conversions
- **Batch processing** - Visual progress indicators

---

Perfect for beginners and power users! 🚀
