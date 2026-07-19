#!/usr/bin/env python3
"""
Image2STL Application Launcher
Main entry point for launching the GUI application.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Launch the Image2STL GUI application."""
    try:
        from src.gui.app import Image2STLGUI
        
        print("=" * 60)
        print("  Image2STL - Image to 3D STL Converter")
        print("=" * 60)
        print()
        print("Launching application...")
        print()
        
        # Create and run the GUI
        app = Image2STLGUI()
        app.main()
        
    except ImportError as e:
        print("Error: Required modules not found.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        print("\nPlease install dependencies with:", file=sys.stderr)
        print("  pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to launch application", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
