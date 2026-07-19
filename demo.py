#!/usr/bin/env python
"""
Image2STL Feature Demo
Demonstrates all new features in the converter.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd: str, description: str):
    """Run a command and show output."""
    print(f"\n{'='*70}")
    print(f"📌 {description}")
    print(f"{'='*70}")
    print(f"$ {cmd}\n")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    IMAGE2STL - FEATURE DEMO                         ║
║                                                                      ║
║ This demo showcases all the enhancements made to the converter       ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    # Make sure demo images exist
    print("Preparing test images...")
    subprocess.run([sys.executable, "create_batch_test_images.py"], 
                   capture_output=True)
    
    demo_dir = Path("demo_output")
    demo_dir.mkdir(exist_ok=True)
    
    demos = [
        (
            f"python -m src.cli.main convert test_images/test_gradient.png {demo_dir}/1_basic.stl",
            "1️⃣  BASIC CONVERSION - Standard grayscale height map"
        ),
        (
            f"python -m src.cli.main convert test_images/checkerboard.png {demo_dir}/2_edge_detection.stl --mode edge_based",
            "2️⃣  EDGE-BASED MODE - Emphasizes edges and features"
        ),
        (
            f"python -m src.cli.main convert test_images/waves.png {demo_dir}/3_inverted.stl --mode inverted",
            "3️⃣  INVERTED MODE - Dark areas become tall"
        ),
        (
            f"python -m src.cli.main convert test_images/radial.png {demo_dir}/4_enhanced.stl --contrast 1.5 --brightness 1.1 --smooth 2.0",
            "4️⃣  ENHANCED PREPROCESSING - Contrast, brightness, smoothing"
        ),
        (
            f"python -m src.cli.main convert test_images/test_gradient.png {demo_dir}/5_with_preview.stl --preview",
            "5️⃣  PREVIEW GENERATION - Creates height maps, comparisons, 3D views"
        ),
        (
            f"python -m src.cli.main preview test_images/waves.png {demo_dir}/ascii_preview/ --format ascii",
            "6️⃣  ASCII PREVIEW - Text-based visualization"
        ),
        (
            f"python -m src.cli.main batch test_images/ {demo_dir}/batch_output/ --height 12 --contrast 1.2",
            "7️⃣  BATCH CONVERSION - Convert multiple images at once"
        ),
    ]
    
    for cmd, description in demos:
        if not run_command(cmd, description):
            print(f"⚠️  Command failed: {cmd}")
    
    print(f"\n{'='*70}")
    print("✅ DEMO COMPLETE!")
    print(f"{'='*70}")
    print(f"\n📁 Output Directory: {demo_dir}/")
    print("\nGenerated Files:")
    
    for file in sorted(demo_dir.rglob("*")):
        if file.is_file():
            size = file.stat().st_size / (1024*1024)  # MB
            print(f"  • {file.relative_to(demo_dir)} ({size:.2f} MB)")
    
    print("\n" + """
╔══════════════════════════════════════════════════════════════════════╗
║ FEATURES DEMONSTRATED:                                              ║
║                                                                      ║
║ ✓ Multiple Height Map Modes (grayscale, inverted, edge_based)       ║
║ ✓ Image Preprocessing (contrast, brightness, smoothing)             ║
║ ✓ Watertight Mesh Generation                                        ║
║ ✓ Preview Generation (PNG and ASCII formats)                        ║
║ ✓ Batch Conversion with Progress Tracking                           ║
║                                                                      ║
║ For more information, see README.md and FEATURES.md                 ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()
