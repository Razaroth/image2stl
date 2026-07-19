"""Easy-to-use GUI for Image2STL converter."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from pathlib import Path
import threading
import sys
from PIL import Image, ImageTk

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.image_processor import ImageProcessor
from services.height_map import HeightMapGenerator
from services.stl_generator import STLGenerator
from services.batch_converter import BatchConverter


class Image2STLGUI:
    """GUI application for Image to STL conversion."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Image2STL Converter")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_single_tab()
        self.create_batch_tab()
        self.create_settings_tab()
        
    def create_single_tab(self):
        """Create single image conversion tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Single Image")
        
        # Title
        title = ttk.Label(frame, text="Convert Single Image", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Input file selection
        input_frame = ttk.LabelFrame(frame, text="Input Image", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(input_frame, textvariable=self.input_file, state="readonly").pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(input_frame, text="Browse...", command=self.browse_input).pack(side="left", padx=5)
        
        # Output file selection
        output_frame = ttk.LabelFrame(frame, text="Output STL File", padding=10)
        output_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(output_frame, textvariable=self.output_file, state="readonly").pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output).pack(side="left", padx=5)
        
        # Settings
        settings_frame = ttk.LabelFrame(frame, text="Settings", padding=10)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Sliders and controls
        self.create_slider(settings_frame, "Scale (XY):", "scale", 50, 300, 100)
        self.create_slider(settings_frame, "Height (mm):", "height", 5, 50, 10)
        self.create_slider(settings_frame, "Resolution:", "resolution", 0.5, 3.0, 1.0, decimals=1)
        self.create_slider(settings_frame, "Smoothing:", "smooth", 0, 5, 1.0, decimals=1)
        self.create_slider(settings_frame, "Contrast:", "contrast", 0.5, 2.0, 1.0, decimals=1)
        self.create_slider(settings_frame, "Brightness:", "brightness", 0.5, 2.0, 1.0, decimals=1)
        self.create_slider(settings_frame, "Base Thickness (mm):", "base", 1, 10, 2.0, decimals=1)
        
        # Mode selection
        mode_frame = ttk.Frame(settings_frame)
        mode_frame.pack(fill="x", pady=5)
        ttk.Label(mode_frame, text="Height Map Mode:", width=20).pack(side="left")
        self.mode_var = tk.StringVar(value="grayscale")
        mode_combo = ttk.Combobox(
            mode_frame, 
            textvariable=self.mode_var,
            values=["grayscale", "inverted", "edge_based", "color_to_height"],
            state="readonly",
            width=20
        )
        mode_combo.pack(side="left", padx=5)
        
        # Checkboxes
        check_frame = ttk.Frame(settings_frame)
        check_frame.pack(fill="x", pady=5)
        
        self.invert_var = tk.BooleanVar()
        ttk.Checkbutton(check_frame, text="Invert Height Map", variable=self.invert_var).pack(anchor="w", padx=5)
        
        self.preview_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(check_frame, text="Generate Preview Images", variable=self.preview_var).pack(anchor="w", padx=5)
        
        # Convert button
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(button_frame, text="Convert to STL", command=self.convert_single).pack(fill="x", pady=5)
        
        # Status
        self.status_frame = ttk.LabelFrame(frame, text="Status", padding=10)
        self.status_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(self.status_frame, height=6, width=80, state="disabled")
        self.status_text.pack(fill="both", expand=True)
        
    def create_batch_tab(self):
        """Create batch conversion tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Batch Convert")
        
        # Title
        title = ttk.Label(frame, text="Batch Convert Images", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Input directory selection
        input_frame = ttk.LabelFrame(frame, text="Input Directory", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(input_frame, textvariable=self.input_dir, state="readonly").pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(input_frame, text="Browse...", command=self.browse_input_dir).pack(side="left", padx=5)
        
        # Output directory selection
        output_frame = ttk.LabelFrame(frame, text="Output Directory", padding=10)
        output_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Entry(output_frame, textvariable=self.output_dir, state="readonly").pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output_dir).pack(side="left", padx=5)
        
        # Settings (same as single)
        settings_frame = ttk.LabelFrame(frame, text="Settings (Applied to All)", padding=10)
        settings_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.create_slider(settings_frame, "Height (mm):", "batch_height", 5, 50, 10)
        self.create_slider(settings_frame, "Contrast:", "batch_contrast", 0.5, 2.0, 1.0, decimals=1)
        self.create_slider(settings_frame, "Smoothing:", "batch_smooth", 0, 5, 1.0, decimals=1)
        
        # Convert button
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(button_frame, text="Convert All", command=self.convert_batch).pack(fill="x", pady=5)
        
        # Progress
        self.progress = ttk.Progressbar(button_frame, mode="determinate")
        self.progress.pack(fill="x", pady=5)
        
        # Status
        self.batch_status_frame = ttk.LabelFrame(frame, text="Status", padding=10)
        self.batch_status_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.batch_status_text = scrolledtext.ScrolledText(self.batch_status_frame, height=8, width=80, state="disabled")
        self.batch_status_text.pack(fill="both", expand=True)
        
    def create_settings_tab(self):
        """Create settings/help tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Help & Settings")
        
        # Help text
        help_text = """
IMAGE2STL CONVERTER - QUICK GUIDE

HEIGHT MAP MODES:
  • Grayscale: Standard brightness-to-height mapping
  • Inverted: Dark areas become tall, bright areas are low
  • Edge-Based: Emphasizes edges and features (great for maps/logos)
  • Color-to-Height: Uses color intensity as height

PARAMETERS:
  • Scale: XY size of the model (50-300)
  • Height: Maximum Z height in mm (5-50)
  • Resolution: Mesh detail level (0.5 = very detailed, 3.0 = coarse)
  • Smoothing: Gaussian blur to reduce noise (0 = sharp, 5 = very smooth)
  • Contrast: Enhance or reduce detail (0.5-2.0)
  • Brightness: Lighten or darken the image (0.5-2.0)
  • Base Thickness: Solid base for stability (1-10 mm)

TIPS FOR BEST RESULTS:
  ✓ Use --contrast 1.5-2.0 for images with subtle details
  ✓ Use --smooth 2.0-3.0 for smooth models, 0.5 for sharp features
  ✓ Lower resolution (0.5-1.0) creates more detail but larger files
  ✓ Generate previews to check before converting
  ✓ Edge-based mode works great for maps and logos

BATCH CONVERSION:
  • Select input folder with images
  • Set output folder
  • Choose settings to apply to all images
  • Click "Convert All"
  • Check status for results

PREVIEW IMAGES:
  When enabled, creates:
  • model_height_map.png - Color visualization
  • model_comparison.png - Original vs height map
  • model_3d_preview.png - 3D model from multiple angles

For more info, see README.md and FEATURES.md
        """
        
        text = scrolledtext.ScrolledText(frame, height=30, width=80, state="normal")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", help_text)
        text.config(state="disabled")
        
    def create_slider(self, parent, label, var_name, from_val, to_val, default, decimals=0):
        """Create a slider with label and value display."""
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)
        
        ttk.Label(frame, text=label, width=20).pack(side="left")
        
        # Create variable
        var = tk.DoubleVar(value=default)
        setattr(self, f"{var_name}_var", var)
        
        # Create slider
        if decimals == 0:
            slider = ttk.Scale(frame, from_=from_val, to=to_val, variable=var, orient="horizontal")
        else:
            slider = ttk.Scale(frame, from_=from_val, to=to_val, variable=var, orient="horizontal")
        slider.pack(side="left", fill="x", expand=True, padx=5)
        
        # Value label
        value_label = ttk.Label(frame, text=f"{default:.1f}" if decimals else str(int(default)), width=8)
        value_label.pack(side="left", padx=5)
        
        # Update label when slider moves
        def update_label(*args):
            val = var.get()
            if decimals:
                value_label.config(text=f"{val:.{decimals}f}")
            else:
                value_label.config(text=str(int(val)))
        
        var.trace("w", update_label)
        
    def browse_input(self):
        """Browse for input image file."""
        file = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"), ("All files", "*.*")]
        )
        if file:
            self.input_file.set(file)
            # Auto-set output
            if not self.output_file.get():
                output = Path(file).parent / (Path(file).stem + ".stl")
                self.output_file.set(str(output))
    
    def browse_output(self):
        """Browse for output STL file."""
        file = filedialog.asksaveasfilename(
            title="Save STL As",
            filetypes=[("STL files", "*.stl"), ("All files", "*.*")],
            defaultextension=".stl"
        )
        if file:
            self.output_file.set(file)
    
    def browse_input_dir(self):
        """Browse for input directory."""
        dir = filedialog.askdirectory(title="Select Input Directory")
        if dir:
            self.input_dir.set(dir)
    
    def browse_output_dir(self):
        """Browse for output directory."""
        dir = filedialog.askdirectory(title="Select Output Directory")
        if dir:
            self.output_dir.set(dir)
    
    def log_status(self, message, text_widget):
        """Log message to status text widget."""
        text_widget.config(state="normal")
        text_widget.insert("end", message + "\n")
        text_widget.see("end")
        text_widget.config(state="disabled")
        self.root.update()
    
    def convert_single(self):
        """Convert single image in thread."""
        if not self.input_file.get() or not self.output_file.get():
            messagebox.showerror("Error", "Please select input and output files")
            return
        
        # Clear status
        self.status_text.config(state="normal")
        self.status_text.delete("1.0", "end")
        self.status_text.config(state="disabled")
        
        # Run in thread
        thread = threading.Thread(target=self._convert_single_thread)
        thread.start()
    
    def _convert_single_thread(self):
        """Convert single image (runs in thread)."""
        try:
            self.log_status("Loading image...", self.status_text)
            
            # Load and process image
            image = ImageProcessor.load_image(self.input_file.get())
            original_image = image.copy()
            image = ImageProcessor.resize_image(image)
            
            if self.contrast_var.get() != 1.0:
                self.log_status(f"Adjusting contrast ({self.contrast_var.get()})...", self.status_text)
                image = ImageProcessor.adjust_contrast(image, self.contrast_var.get())
            
            if self.brightness_var.get() != 1.0:
                self.log_status(f"Adjusting brightness ({self.brightness_var.get()})...", self.status_text)
                image = ImageProcessor.adjust_brightness(image, self.brightness_var.get())
            
            image = ImageProcessor.normalize_image(image)
            
            if self.smooth_var.get() > 0:
                self.log_status(f"Smoothing (sigma={self.smooth_var.get()})...", self.status_text)
                image = ImageProcessor.apply_smoothing(image, sigma=self.smooth_var.get())
            
            if self.invert_var.get():
                self.log_status("Inverting height map...", self.status_text)
                image = ImageProcessor.invert_image(image)
            
            self.log_status(f"Generating height map ({self.mode_var.get()} mode)...", self.status_text)
            X, Y, Z = HeightMapGenerator.generate_height_map_advanced(
                image,
                max_height=self.height_var.get(),
                scale_xy=self.scale_var.get(),
                resolution=self.resolution_var.get(),
                mode=self.mode_var.get(),
            )
            
            self.log_status("Adding base thickness...", self.status_text)
            Z = HeightMapGenerator.apply_base_thickness(Z, base_thickness=self.base_var.get())
            
            self.log_status("Creating 3D mesh...", self.status_text)
            mesh = STLGenerator.create_mesh_from_height_map(X, Y, Z)
            
            self.log_status("Making mesh watertight...", self.status_text)
            mesh = STLGenerator.make_watertight(mesh)
            
            self.log_status("Adding base...", self.status_text)
            mesh = STLGenerator.add_base_to_mesh(mesh, base_height=self.base_var.get())
            
            info = STLGenerator.get_mesh_info(mesh)
            
            self.log_status("Saving STL file...", self.status_text)
            STLGenerator.save_stl(mesh, self.output_file.get())
            
            self.log_status("\n✓ Conversion Successful!", self.status_text)
            self.log_status(f"Output: {self.output_file.get()}", self.status_text)
            self.log_status(f"Vertices: {info['vertices']}", self.status_text)
            self.log_status(f"Faces: {info['faces']}", self.status_text)
            self.log_status(f"Volume: {info['volume']:.2f} mm³", self.status_text)
            self.log_status(f"Watertight: {info['is_watertight']}", self.status_text)
            
            messagebox.showinfo("Success", "Conversion completed!")
            
        except Exception as e:
            self.log_status(f"\n✗ Error: {str(e)}", self.status_text)
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
    
    def convert_batch(self):
        """Convert batch in thread."""
        if not self.input_dir.get() or not self.output_dir.get():
            messagebox.showerror("Error", "Please select input and output directories")
            return
        
        # Clear status and progress
        self.batch_status_text.config(state="normal")
        self.batch_status_text.delete("1.0", "end")
        self.batch_status_text.config(state="disabled")
        self.progress["value"] = 0
        
        # Run in thread
        thread = threading.Thread(target=self._convert_batch_thread)
        thread.start()
    
    def _convert_batch_thread(self):
        """Convert batch (runs in thread)."""
        try:
            self.log_status("Starting batch conversion...", self.batch_status_text)
            
            params = {
                'height': self.batch_height_var.get(),
                'contrast': self.batch_contrast_var.get(),
                'smooth': self.batch_smooth_var.get(),
            }
            
            def progress_callback(current, total, filename):
                self.log_status(f"[{current}/{total}] {filename}...", self.batch_status_text)
                self.progress["value"] = (current / total) * 100
                self.root.update()
            
            results = BatchConverter.convert_directory(
                self.input_dir.get(),
                self.output_dir.get(),
                progress_callback=progress_callback,
                conversion_params=params,
            )
            
            self.log_status("\n" + "="*60, self.batch_status_text)
            self.log_status("BATCH CONVERSION RESULTS", self.batch_status_text)
            self.log_status("="*60, self.batch_status_text)
            
            success = sum(1 for r in results if r['status'] == 'success')
            errors = len(results) - success
            
            self.log_status(f"Total: {len(results)} | Success: {success} | Errors: {errors}\n", self.batch_status_text)
            
            for result in results:
                if result['status'] == 'success':
                    self.log_status(f"✓ {Path(result['input']).name}", self.batch_status_text)
                else:
                    self.log_status(f"✗ {Path(result.get('input', 'Unknown')).name} - {result['error']}", self.batch_status_text)
            
            self.progress["value"] = 100
            messagebox.showinfo("Complete", f"Batch conversion complete!\nSuccess: {success}, Errors: {errors}")
            
        except Exception as e:
            self.log_status(f"\n✗ Error: {str(e)}", self.batch_status_text)
            messagebox.showerror("Error", f"Batch conversion failed: {str(e)}")


def main():
    root = tk.Tk()
    app = Image2STLGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
