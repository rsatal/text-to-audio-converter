import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from azure_tts import text_to_speech

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Azure OpenAI Text-to-Speech Converter")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Azure credentials section
        creds_frame = ttk.LabelFrame(main_frame, text="Azure OpenAI Credentials", padding="10")
        creds_frame.pack(fill="x", pady=10)
        
        ttk.Label(creds_frame, text="API Key:").grid(row=0, column=0, sticky="w", pady=5)
        self.api_key_var = tk.StringVar(value=os.environ.get("AZURE_OPENAI_API_KEY", ""))
        self.api_key_entry = ttk.Entry(creds_frame, textvariable=self.api_key_var, width=40, show="*")
        self.api_key_entry.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(creds_frame, text="Endpoint:").grid(row=1, column=0, sticky="w", pady=5)
        self.endpoint_var = tk.StringVar(value=os.environ.get("AZURE_OPENAI_ENDPOINT", ""))
        self.endpoint_entry = ttk.Entry(creds_frame, textvariable=self.endpoint_var, width=40)
        self.endpoint_entry.grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Label(creds_frame, text="API Version:").grid(row=2, column=0, sticky="w", pady=5)
        self.api_version_var = tk.StringVar(value=os.environ.get("API_VERSION", "2025-01-01-preview"))
        self.api_version_entry = ttk.Entry(creds_frame, textvariable=self.api_version_var, width=20)
        self.api_version_entry.grid(row=2, column=1, sticky="w", padx=5)
        
        # Voice selection
        ttk.Label(creds_frame, text="Voice:").grid(row=3, column=0, sticky="w", pady=5)
        self.voice_var = tk.StringVar(value="alloy")
        voices = [
            "alloy",
            "echo",
            "fable",
            "onyx",
            "nova",
            "shimmer"
        ]
        self.voice_combo = ttk.Combobox(creds_frame, values=voices, textvariable=self.voice_var, width=30)
        self.voice_combo.grid(row=3, column=1, sticky="w", padx=5)
        
        # Text input section
        text_frame = ttk.LabelFrame(main_frame, text="Text Input", padding="10")
        text_frame.pack(fill="both", expand=True, pady=10)
        
        self.text_input = tk.Text(text_frame, wrap="word", height=10)
        self.text_input.pack(fill="both", expand=True, pady=5)
        
        # Output file section
        output_frame = ttk.Frame(main_frame, padding="10")
        output_frame.pack(fill="x", pady=10)
        
        ttk.Label(output_frame, text="Output File:").grid(row=0, column=0, sticky="w")
        self.output_file_var = tk.StringVar(value=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.wav"))
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_file_var, width=50)
        self.output_entry.grid(row=0, column=1, padx=5)
        
        self.browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output_file)
        self.browse_btn.grid(row=0, column=2)
        
        # Buttons section
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(btn_frame, textvariable=self.status_var)
        self.status_label.pack(side="left", padx=10)
        
        self.convert_btn = ttk.Button(btn_frame, text="Convert to Speech", command=self.start_conversion)
        self.convert_btn.pack(side="right", padx=10)
    
    def browse_output_file(self):
        initial_dir = os.path.dirname(self.output_file_var.get())
        filename = filedialog.asksaveasfilename(
            title="Save Audio File",
            initialdir=initial_dir,
            initialfile="output.wav",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)
    
    def start_conversion(self):
        # Get values from UI
        api_key = self.api_key_var.get().strip()
        endpoint = self.endpoint_var.get().strip()
        api_version = self.api_version_var.get().strip()
        voice = self.voice_var.get()
        text = self.text_input.get("1.0", "end-1c").strip()
        output_file = self.output_file_var.get()
        
        # Validate inputs
        if not api_key:
            messagebox.showerror("Error", "Please enter your Azure OpenAI API key")
            return
        
        if not endpoint:
            messagebox.showerror("Error", "Please enter your Azure OpenAI endpoint")
            return
        
        if not text:
            messagebox.showerror("Error", "Please enter some text to convert")
            return
        
        # Disable UI during conversion
        self.convert_btn.config(state="disabled")
        self.status_var.set("Converting...")
        
        # Run conversion in a separate thread to avoid freezing the UI
        threading.Thread(
            target=self._run_conversion,
            args=(text, output_file, api_key, endpoint, api_version, voice),
            daemon=True
        ).start()
    
    def _run_conversion(self, text, output_file, api_key, endpoint, api_version, voice):
        try:
            success = text_to_speech(
                text=text,
                output_file=output_file,
                api_key=api_key,
                endpoint=endpoint,
                api_version=api_version,
                voice_name=voice
            )
            
            # Update UI on the main thread
            self.root.after(0, self._update_ui_after_conversion, success, output_file)
            
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _update_ui_after_conversion(self, success, output_file):
        self.convert_btn.config(state="normal")
        
        if success:
            self.status_var.set("Conversion completed!")
            messagebox.showinfo("Success", f"Speech generated successfully!\nSaved to: {output_file}")
        else:
            self.status_var.set("Conversion failed. See error details.")
    
    def _show_error(self, error_msg):
        self.convert_btn.config(state="normal")
        self.status_var.set("Error occurred")
        messagebox.showerror("Error", f"An error occurred:\n{error_msg}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()