import requests
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from urllib.parse import urlparse, unquote

# ---------- Configuration ----------
CONFIG_FILE = "relay_config.json"
MAX_FILE_SIZE_MB = 50

# ---------- Helper Functions ----------
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"script_url": "", "folder_id": ""}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def extract_filename_from_url(url):
    parsed = urlparse(url)
    path = unquote(parsed.path)
    filename = os.path.basename(path)
    if not filename or '.' not in filename:
        return "downloaded_file"
    return filename

def get_file_size(url):
    try:
        head_resp = requests.head(url, allow_redirects=True, timeout=10)
        size = head_resp.headers.get('Content-Length')
        if size:
            return int(size)
    except:
        pass
    return None

# ---------- Tooltip Class ----------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind('<Enter>', self.show_tip)
        widget.bind('<Leave>', self.hide_tip)
    
    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        style = ttk.Style()
        style.configure("Tooltip.TLabel", background="#ffffcc", foreground="#666666", font=("Segoe UI", 9))
        label = ttk.Label(tw, text=self.text, style="Tooltip.TLabel", wraplength=300, justify=tk.LEFT)
        label.pack(padx=2, pady=2)
    
    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

# ---------- Entry with Placeholder ----------
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", color='grey', **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._set_placeholder)
        
        if not self.get():
            self._set_placeholder()
    
    def _clear_placeholder(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color
    
    def _set_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

# ---------- Main Application ----------
class DriveRelayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Drive Relay Downloader")
        self.root.geometry("750x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        self.config = load_config()
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Header
        tk.Label(main_frame, text="Google Drive Relay Downloader", 
                 font=("Segoe UI", 16, "bold"), bg="#f0f0f0", fg="#2c3e50").pack(anchor=tk.W, pady=(0,5))
        tk.Label(main_frame, text="Download any file directly to your Google Drive via Apps Script relay",
                 font=("Segoe UI", 9), bg="#f0f0f0", fg="#555555").pack(anchor=tk.W, pady=(0,15))
        
        tk.Frame(main_frame, height=2, bg="#cccccc").pack(fill=tk.X, pady=5)
        
        form = tk.Frame(main_frame, bg="#f0f0f0")
        form.pack(fill=tk.X, pady=10)
        
        form.columnconfigure(0, weight=0)
        form.columnconfigure(1, weight=1)
        
        # Row 0: Apps Script URL
        lbl_script = tk.Label(form, text="Apps Script URL:", font=("Segoe UI", 10), bg="#f0f0f0", anchor=tk.W)
        lbl_script.grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0,10))
        ToolTip(lbl_script, "The URL of your Google Apps Script web app (the relay).")
        
        self.entry_script_url = PlaceholderEntry(form, placeholder="e.g., https://script.google.com/macros/s/.../exec", 
                                                  font=("Segoe UI", 10), relief=tk.SOLID, bd=1)
        self.entry_script_url.grid(row=0, column=1, sticky=tk.EW, pady=8)
        # Load saved value if any
        saved_url = self.config.get("script_url", "")
        if saved_url:
            self.entry_script_url.delete(0, tk.END)
            self.entry_script_url.insert(0, saved_url)
            self.entry_script_url['fg'] = 'black'
        ToolTip(self.entry_script_url, "Paste the web app URL from your Google Apps Script deployment.")
        
        # Row 1: Folder ID
        lbl_folder = tk.Label(form, text="Drive Folder ID (optional):", font=("Segoe UI", 10), bg="#f0f0f0", anchor=tk.W)
        lbl_folder.grid(row=1, column=0, sticky=tk.W, pady=8, padx=(0,10))
        ToolTip(lbl_folder, "The ID of the Google Drive folder where files will be saved.\nLeave empty to use the default folder set in the script.")
        
        self.entry_folder_id = PlaceholderEntry(form, placeholder="Enter Google Drive folder ID (optional)", 
                                                 font=("Segoe UI", 10), relief=tk.SOLID, bd=1)
        self.entry_folder_id.grid(row=1, column=1, sticky=tk.EW, pady=8)
        saved_folder = self.config.get("folder_id", "")
        if saved_folder:
            self.entry_folder_id.delete(0, tk.END)
            self.entry_folder_id.insert(0, saved_folder)
            self.entry_folder_id['fg'] = 'black'
        ToolTip(self.entry_folder_id, "Example: 1xT3pnZ-5BJBFE8bxArkmiqAT0i_jQ81i\nFind it in the URL of your Drive folder.")
        
        hint_folder = tk.Label(form, text="Leave empty to use default folder from script", 
                               font=("Segoe UI", 8), bg="#f0f0f0", fg="#777777")
        hint_folder.grid(row=2, column=1, sticky=tk.W, padx=(0,0), pady=(0,5))
        
        # Row 3: File URL
        lbl_url = tk.Label(form, text="File URL:", font=("Segoe UI", 10), bg="#f0f0f0", anchor=tk.W)
        lbl_url.grid(row=3, column=0, sticky=tk.W, pady=8, padx=(0,10))
        ToolTip(lbl_url, "Direct download link to the file you want to save to Drive.")
        
        self.entry_url = PlaceholderEntry(form, placeholder="https://example.com/file.pdf", 
                                           font=("Segoe UI", 10), relief=tk.SOLID, bd=1)
        self.entry_url.grid(row=3, column=1, sticky=tk.EW, pady=8)
        ToolTip(self.entry_url, "Make sure the link is publicly accessible or the relay can reach it.")
        
        # Row 4: Filename
        lbl_filename = tk.Label(form, text="Save as (optional):", font=("Segoe UI", 10), bg="#f0f0f0", anchor=tk.W)
        lbl_filename.grid(row=4, column=0, sticky=tk.W, pady=8, padx=(0,10))
        ToolTip(lbl_filename, "Custom name for the file on Google Drive.\nLeave empty to auto-extract from URL.")
        
        self.entry_filename = PlaceholderEntry(form, placeholder="my_custom_filename.pdf", 
                                                font=("Segoe UI", 10), relief=tk.SOLID, bd=1)
        self.entry_filename.grid(row=4, column=1, sticky=tk.EW, pady=8)
        ToolTip(self.entry_filename, "For example: report.pdf\nIf empty, the filename will be taken from the URL.")
        
        hint_filename = tk.Label(form, text="Leave empty to auto-extract filename from URL. Example: https://example.com/sample.pdf → sample.pdf",
                                 font=("Segoe UI", 8), bg="#f0f0f0", fg="#2980b9")
        hint_filename.grid(row=5, column=1, sticky=tk.W, padx=(0,0), pady=(0,10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=500)
        self.progress.pack(pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(main_frame, textvariable=self.status_var, font=("Segoe UI", 9), 
                                      bg="#f0f0f0", fg="#2e7d32")
        self.status_label.pack(anchor=tk.W, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.pack(pady=15)
        
        self.btn_download = tk.Button(btn_frame, text="📥 Download to Drive", command=self.send_download_request,
                                      font=("Segoe UI", 11, "bold"), bg="#2196f3", fg="white", 
                                      padx=20, pady=8, relief=tk.RAISED, bd=0, cursor="hand2")
        self.btn_download.pack(side=tk.LEFT, padx=10)
        
        self.btn_save = tk.Button(btn_frame, text="⚙️ Save Settings", command=self.save_settings,
                                  font=("Segoe UI", 10), bg="#607d8b", fg="white", 
                                  padx=15, pady=8, relief=tk.RAISED, bd=0, cursor="hand2")
        self.btn_save.pack(side=tk.LEFT, padx=10)
        
        footer = tk.Label(main_frame, text=f"Files are saved directly to your Google Drive. Maximum file size: {MAX_FILE_SIZE_MB} MB (Google Apps Script limit).",
                          font=("Segoe UI", 8), bg="#f0f0f0", fg="#888888")
        footer.pack(side=tk.BOTTOM, pady=5)
        
        # Hover effects
        self.btn_download.bind("<Enter>", lambda e: self.btn_download.config(bg="#0b7dda"))
        self.btn_download.bind("<Leave>", lambda e: self.btn_download.config(bg="#2196f3"))
        self.btn_save.bind("<Enter>", lambda e: self.btn_save.config(bg="#455a64"))
        self.btn_save.bind("<Leave>", lambda e: self.btn_save.config(bg="#607d8b"))
        
    def save_settings(self):
        script_url = self.entry_script_url.get()
        if script_url == self.entry_script_url.placeholder:
            script_url = ""
        folder_id = self.entry_folder_id.get()
        if folder_id == self.entry_folder_id.placeholder:
            folder_id = ""
        
        self.config["script_url"] = script_url.strip()
        self.config["folder_id"] = folder_id.strip()
        save_config(self.config)
        self.status_var.set("✓ Settings saved")
        self.status_label.config(fg="#2e7d32")
        self.root.after(2000, lambda: self.status_var.set("Ready") and self.status_label.config(fg="#2e7d32"))
    
    def send_download_request(self):
        url = self.entry_url.get()
        if url == self.entry_url.placeholder:
            url = ""
        filename = self.entry_filename.get()
        if filename == self.entry_filename.placeholder:
            filename = ""
        script_url = self.entry_script_url.get()
        if script_url == self.entry_script_url.placeholder:
            script_url = ""
        folder_id = self.entry_folder_id.get()
        if folder_id == self.entry_folder_id.placeholder:
            folder_id = ""
        
        url = url.strip()
        filename = filename.strip()
        script_url = script_url.strip()
        folder_id = folder_id.strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a file URL")
            return
        if not script_url:
            messagebox.showerror("Error", "Please enter the Apps Script URL")
            return
        
        self.status_var.set("Checking file size...")
        self.status_label.config(fg="#1976d2")
        self.root.update()
        
        file_size = get_file_size(url)
        if file_size is not None:
            size_mb = file_size / (1024 * 1024)
            if size_mb > MAX_FILE_SIZE_MB:
                msg = (f"File size ({size_mb:.1f} MB) exceeds the {MAX_FILE_SIZE_MB} MB limit.\n"
                       "Google Apps Script cannot download files larger than 50 MB.\n\n"
                       "Do you still want to try?")
                if not messagebox.askyesno("File Too Large", msg, icon='warning'):
                    self.status_var.set("Cancelled (file too large)")
                    self.status_label.config(fg="#c62828")
                    return
        
        if not filename:
            filename = extract_filename_from_url(url)
            self.status_var.set(f"Auto-detected filename: {filename}")
            self.status_label.config(fg="#1976d2")
            self.root.update()
        
        self.btn_download.config(state=tk.DISABLED, bg="#9e9e9e")
        self.progress.start(10)
        self.status_var.set("Contacting relay...")
        self.status_label.config(fg="#1976d2")
        self.root.update()
        
        try:
            payload = {"url": url, "fileName": filename}
            if folder_id:
                payload["folderId"] = folder_id
            
            response = requests.post(script_url, json=payload, timeout=300)
            result = response.json()
            
            if result.get("success"):
                file_url = result.get("fileUrl")
                messagebox.showinfo("Success", f"✅ File saved to Drive!\n\nFile name: {filename}\n\nFile URL:\n{file_url}")
                self.status_var.set("✓ Download completed successfully!")
                self.status_label.config(fg="#2e7d32")
                self.entry_url.delete(0, tk.END)
                self.entry_url._set_placeholder()
                self.entry_filename.delete(0, tk.END)
                self.entry_filename._set_placeholder()
            else:
                error_msg = result.get("error", "Unknown error")
                if "size" in error_msg.lower() or "limit" in error_msg.lower():
                    error_msg += f"\n\nNote: Google Apps Script cannot download files larger than {MAX_FILE_SIZE_MB} MB."
                messagebox.showerror("Relay Error", f"Error from relay:\n{error_msg}")
                self.status_var.set("✗ Error from relay")
                self.status_label.config(fg="#c62828")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("✗ Request failed")
            self.status_label.config(fg="#c62828")
        finally:
            self.progress.stop()
            self.btn_download.config(state=tk.NORMAL, bg="#2196f3")
            self.root.update()

# ---------- Run ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = DriveRelayApp(root)
    root.mainloop()