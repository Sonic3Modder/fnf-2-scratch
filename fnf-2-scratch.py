import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import os
import re
import sys

class CSSParser:
    """Simple CSS parser to apply styles to Tkinter widgets"""
    def __init__(self, css_file):
        self.styles = {}
        self.parse_css(css_file)
    
    def parse_css(self, css_file):
        try:
            with open(css_file, 'r') as file:
                css_content = file.read()
            
            # Extract CSS rules using regex
            pattern = r'\.([a-zA-Z0-9-]+)\s*\{([^}]+)\}'
            matches = re.findall(pattern, css_content)
            
            for class_name, properties in matches:
                property_dict = {}
                for prop in properties.strip().split(';'):
                    if ':' in prop:
                        key, value = prop.split(':', 1)
                        property_dict[key.strip()] = value.strip()
                self.styles[class_name] = property_dict
        except Exception as e:
            print(f"Error parsing CSS: {str(e)}")
    
    def get_style(self, class_name):
        return self.styles.get(class_name, {})
    
    def apply_to_widget(self, widget, class_name):
        style = self.get_style(class_name)
        
        # Apply background color
        if 'background-color' in style:
            widget.configure(bg=style['background-color'])
        
        # Apply text color
        if 'color' in style:
            if hasattr(widget, 'configure') and 'fg' in widget.configure():
                widget.configure(fg=style['color'])
        
        # Apply font
        font_family = style.get('font-family', '').strip('"\'')
        font_size = style.get('font-size', '12').replace('px', '')
        font_weight = 'bold' if style.get('font-weight') == 'bold' else 'normal'
        
        try:
            if font_family or font_size:
                widget.configure(font=(font_family, int(font_size), font_weight))
        except:
            pass
        
        # Apply padding
        if 'padding' in style:
            padding = style['padding'].replace('px', '')
            try:
                padding = int(padding)
                widget.configure(padx=padding, pady=padding)
            except:
                pass
        
        # Apply border radius (not directly supported in Tkinter)
        
        # Apply other properties based on widget type
        if isinstance(widget, tk.Button):
            if 'background-color' in style:
                widget.configure(activebackground=self._darken_color(style['background-color']))
    
    def _darken_color(self, color):
        """Darken a hex color by 20%"""
        if color.startswith('#') and len(color) == 7:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = max(0, int(r * 0.8))
            g = max(0, int(g * 0.8))
            b = max(0, int(b * 0.8))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        return color

class FNFtoScratchConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("FNF to Scratch Chart Converter")
        self.window.geometry("600x500")
        
        # Get the directory where the script is running from
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (compiled with PyInstaller)
            self.app_path = sys._MEIPASS
        else:
            # If the application is run as a script
            self.app_path = os.path.dirname(os.path.abspath(__file__))
        
        # Look for CSS file in the application directory
        css_file = os.path.join(self.app_path, "fnf-scratch-styles.css")
        
        # Check if CSS file exists
        if not os.path.exists(css_file):
            messagebox.showerror("Error", f"CSS file not found: {css_file}\nPlease ensure 'fnf-scratch-styles.css' is in the same directory as the application.")
            sys.exit(1)
        
        # Load CSS styles
        self.css = CSSParser(css_file)
        
        # Apply main window style
        self.css.apply_to_widget(self.window, "window")
        
        # Create header
        self.header_frame = tk.Frame(self.window)
        self.css.apply_to_widget(self.header_frame, "header")
        self.header_frame.pack(fill=tk.X)
        
        self.logo_label = tk.Label(self.header_frame, text="🎵 FNF ➡️ Scratch Converter 🎮")
        self.css.apply_to_widget(self.logo_label, "header-text")
        self.logo_label.pack(pady=10)
        
        # Create main frame
        self.main_frame = tk.Frame(self.window)
        self.css.apply_to_widget(self.main_frame, "content")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Status indicators
        self.status_frame = tk.Frame(self.main_frame)
        self.css.apply_to_widget(self.status_frame, "window")
        self.status_frame.pack(fill=tk.X, pady=10)
        
        self.file_status = tk.Label(self.status_frame, text="No File Loaded")
        self.css.apply_to_widget(self.file_status, "label")
        self.file_status.pack(side=tk.LEFT, padx=5)
        
        self.chart_type_label = tk.Label(self.status_frame, text="Type: None")
        self.css.apply_to_widget(self.chart_type_label, "label")
        self.chart_type_label.pack(side=tk.RIGHT, padx=5)
        
        # Create buttons frame
        self.buttons_frame = tk.Frame(self.main_frame)
        self.css.apply_to_widget(self.buttons_frame, "window")
        self.buttons_frame.pack(fill=tk.X)
        
        # Load JSON button
        self.load_btn = tk.Button(self.buttons_frame, text="Load FNF Chart (JSON)", command=self.load_chart)
        self.css.apply_to_widget(self.load_btn, "button-fnf")
        self.load_btn.pack(fill=tk.X, pady=10)
        
        # Load TXT button
        self.load_txt_btn = tk.Button(self.buttons_frame, text="Load Text Chart (TXT)", command=self.load_text_chart)
        self.css.apply_to_widget(self.load_txt_btn, "button-text")
        self.load_txt_btn.pack(fill=tk.X, pady=10)
        
        # Separator
        ttk.Separator(self.main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Options frame
        self.options_frame = tk.Frame(self.main_frame)
        self.css.apply_to_widget(self.options_frame, "window")
        self.options_frame.pack(fill=tk.X, pady=10)
        
        # Default velocity option
        self.velocity_frame = tk.Frame(self.options_frame)
        self.css.apply_to_widget(self.velocity_frame, "window")
        self.velocity_frame.pack(pady=5)
        
        self.velocity_label = tk.Label(self.velocity_frame, text="Default Velocity:")
        self.css.apply_to_widget(self.velocity_label, "label")
        self.velocity_label.pack(side=tk.LEFT, padx=5)
        
        self.velocity_var = tk.StringVar(value="171")  # Default velocity
        self.velocity_entry = tk.Entry(self.velocity_frame, textvariable=self.velocity_var, width=10)
        self.css.apply_to_widget(self.velocity_entry, "entry")
        self.velocity_entry.pack(side=tk.LEFT, padx=5)
        
        # Convert button
        self.convert_btn = tk.Button(self.main_frame, text="⚡ Convert to Scratch Format ⚡", command=self.convert)
        self.css.apply_to_widget(self.convert_btn, "button-scratch")
        self.convert_btn.pack(fill=tk.X, pady=20)
        
        # Preview frame
        self.preview_frame = tk.Frame(self.main_frame)
        self.css.apply_to_widget(self.preview_frame, "window")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.preview_label = tk.Label(self.preview_frame, text="Chart Preview (First 5 notes)")
        self.css.apply_to_widget(self.preview_label, "label-header")
        self.preview_label.pack(pady=5)
        
        self.preview_text = tk.Text(self.preview_frame, height=5, width=50)
        self.css.apply_to_widget(self.preview_text, "preview")
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Footer with credits
        self.footer = tk.Label(self.window, text="Made with ❤️ for FNF and Scratch communities")
        self.css.apply_to_widget(self.footer, "footer")
        self.footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Initialize variables
        self.chart_data = None
        self.chart_type = None  # "json" or "txt"
        self.file_path = None
    


    def load_chart(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.chart_data = json.load(file)
                self.chart_type = "json"
                self.file_path = file_path
                self.update_status()
                messagebox.showinfo("Success", "JSON Chart loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load chart file: {str(e)}")

    def load_text_chart(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    parsed_data = []
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        # Expected format: {time}: {lane}: {}: {velocity}
                        parts = line.split("}")
                        if len(parts) >= 4:
                            time_part = parts[0].strip("{")
                            lane_part = parts[1].strip("{}")
                            velocity_part = parts[3].strip("{}")
                            
                            # Extract numeric values
                            time = float(time_part) if time_part else 0
                            lane = int(lane_part) if lane_part else 0
                            velocity = float(velocity_part) if velocity_part and velocity_part != "" else 0
                            
                            parsed_data.append({
                                "time": time,
                                "lane": lane,
                                "velocity": velocity
                            })
                    
                    self.chart_data = parsed_data
                    self.chart_type = "txt"
                    self.file_path = file_path
                    self.update_status()
                    messagebox.showinfo("Success", f"Text Chart loaded successfully! {len(parsed_data)} notes found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load text chart: {str(e)}")

    def update_status(self):
        if self.file_path:
            filename = os.path.basename(self.file_path)
            self.file_status.config(text=f"Loaded: {filename}")
        else:
            self.file_status.config(text="No File Loaded")
            
        if self.chart_type:
            self.chart_type_label.config(text=f"Type: {self.chart_type.upper()}")
        else:
            self.chart_type_label.config(text="Type: None")
            
        # Update preview if data exists
        if self.chart_data:
            self.update_preview()
    
    def update_preview(self):
        self.preview_text.delete(1.0, tk.END)
        
        if self.chart_type == "json":
            # Format JSON preview
            try:
                song = self.chart_data.get("song", {})
                notes = song.get("notes", [])
                count = 0
                preview_text = ""
                
                for section in notes:
                    for note in section.get("sectionNotes", []):
                        time = note[0] / 1000  # Convert to seconds
                        lane = note[1] % 4  # Ensure lane is 0-3
                        
                        preview_text += f"{{{time}}}: {{{lane+1}}}: {{}}: {{171}}\n"
                        count += 1
                        if count >= 5:  # Only show 5 notes
                            break
                    if count >= 5:
                        break
                
                self.preview_text.insert(1.0, preview_text)
            except Exception as e:
                self.preview_text.insert(1.0, f"Error generating preview: {str(e)}")
        
        elif self.chart_type == "txt":
            # Format text preview
            preview_notes = self.chart_data[:5]  # First 5 notes
            preview_text = ""
            
            for note in preview_notes:
                time = note["time"]
                lane = note["lane"]
                velocity = note.get("velocity", 0)
                preview_text += f"{{{time}}}: {{{lane}}}: {{}}: {{{velocity}}}\n"
            
            self.preview_text.insert(1.0, preview_text)

    def convert(self):
        if not self.chart_data:
            messagebox.showerror("Error", "Please load a chart first!")
            return

        try:
            scratch_data = []
            default_velocity = int(self.velocity_var.get()) if self.velocity_var.get().isdigit() else 171
            
            if self.chart_type == "json":
                # Get notes from JSON chart
                song = self.chart_data.get("song", {})
                notes = song.get("notes", [])
                
                for section in notes:
                    for note in section.get("sectionNotes", []):
                        time = note[0] / 1000  # Convert to seconds
                        lane = note[1] % 4  # Ensure lane is 0-3
                        duration = note[2] / 1000 if note[2] else 0
                        
                        # Only include opponent notes if specified
                        if not section.get("mustHitSection", True) or lane >= 4:
                            # Adjust lane for opponent notes (lane 4-7 -> 0-3)
                            if lane >= 4:
                                lane -= 4
                            
                            # Convert to Scratch format (format is based on your sample)
                            scratch_note = {
                                "time": time,
                                "lane": lane + 1,  # Adjust lane to match 1-4 format seen in example
                                "velocity": default_velocity
                            }
                            scratch_data.append(scratch_note)
            
            elif self.chart_type == "txt":
                # Text chart format is already parsed and similar to Scratch format
                scratch_data = self.chart_data
            
            # Format the output as text similar to the example
            output_lines = []
            for note in scratch_data:
                time = note["time"]
                lane = note["lane"]
                velocity = note.get("velocity", default_velocity)
                output_lines.append(f"{{{time}}}: {{{lane}}}: {{}}: {{{velocity}}}")
            
            # Save converted file
            save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt")])
            if save_path:
                with open(save_path, 'w') as file:
                    file.write("\n".join(output_lines))
                messagebox.showinfo("Success", "Chart converted successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    converter = FNFtoScratchConverter()
    converter.run()
