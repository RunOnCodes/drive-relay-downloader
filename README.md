# 📥 Google Drive Relay Downloader

A desktop GUI tool that downloads any file (from any public URL) and saves it directly to your **Google Drive** – using a Google Apps Script as a relay.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Apps Script](https://img.shields.io/badge/Google-AppsScript-yellow)

## 🌐 Available Languages

* [English 🇺🇸](README.md)
* [فارسی 🇮🇷](README_FA.md)
* [Türkçe 🇹🇷](README_TR.md)

---

## ✨ Features

* **Bypass Local Storage:** The file goes directly from the source URL to your Google Drive. It never downloads to your local hard drive.
* **Simple GUI:** An easy-to-use desktop interface built with Tkinter.
* **Auto-Extraction:** Automatically extracts the filename from the URL if a custom name isn't provided.
* **Custom Folders:** Optionally specify different Google Drive folder IDs directly in the GUI to sort your downloads on the fly.
* **Silent Launch:** Includes a VBScript wrapper for Windows users to launch the app without a lingering command prompt window.

---

## 🚀 How It Works

1.  You provide a **file URL** (e.g., `https://example.com/file.pdf`).
2.  The Python GUI sends the URL + desired filename to your **Google Apps Script web app**.
3.  The Apps Script validates the inputs, fetches the remote file, and saves it into your **Google Drive folder**.
4.  The script returns a success response and the GUI displays the new Drive file URL.

---

## 🛠️ Setup Instructions

### Prerequisites

* **Python 3.7+** installed on your system

### 1. Install Required Dependencies

This application requires two key components:
- **`requests`** - Python library for HTTP requests (installs via pip)
- **`Tkinter`** - GUI library (usually pre-installed with Python)

#### Option A: Using requirements.txt (Recommended)

```bash
pip install -r requirements.txt
```

#### Option B: Manual Installation

```bash
pip install requests
```

#### Install Tkinter by Operating System:

**Windows & macOS:**
- Tkinter is pre-installed with Python. No additional action needed.

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

### 2. Deploy the Google Apps Script

* Open [script.google.com](https://script.google.com) and create a new project.
* Replace the default code with the content of [`ScriptToDeploy.gs`](ScriptToDeploy.gs).
* **Modify the folder ID** inside the script:  
    `const folderId = 'YOUR_DRIVE_FOLDER_ID';`  
    *(Find your folder ID in its Drive URL: `https://drive.google.com/drive/folders/THIS_IS_THE_ID`)*
* Deploy as a **Web App**:
    * Execute as: **Me**
    * Who has access: **Anyone** (or "Anyone with link" – the tool needs to be able to reach it).
    * Click **Deploy** → **New deployment** → **Web app**.  
    * Copy the **deployment URL** (looks like `https://script.google.com/macros/s/.../exec`).

### 3. Configure the Python Application

* Edit `relay_config.json` and paste your Apps Script URL:  
    ```json
    {
      "script_url": "https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec",
      "folder_id": ""
    }
    ```
    *(Alternatively, you can just enter the URL directly into the GUI and click "Save Settings").*

---

## 💻 Usage

### Running the App

You have two ways to start the application:
1.  **Standard Launch:** Run the Python script directly from your terminal or command prompt:
    ```bash
    python drive_relay_gui.py
    ```
2.  **Silent Launch (Windows Only):** Double-click [`launch_gui.vbs`](launch_gui.vbs). This script uses `pythonw` to run the graphical interface silently in the background without keeping a command prompt window open.

### Using the Interface

* **Apps Script URL:** Paste the web app URL you generated in Step 2.
* **Drive Folder ID (Optional):** If you want to save a specific file to a different folder than the default one hardcoded in your Apps Script, paste the new folder ID here.
* **File URL:** The direct download link to the file.
* **Save as (Optional):** Provide a custom name (e.g., `report_2026.pdf`). If left blank, the app will auto-detect the name from the URL.
* Click **"📥 Download to Drive"**.

<img width="933" height="759" alt="image" src="https://github.com/user-attachments/assets/7d1c6ade-18dd-4566-97a0-2860379c2561" />

---

## ⚠️ Limitations & Notes

* **50 MB File Limit:** Google Apps Script has a strict memory limit for fetching and manipulating blobs (`UrlFetchApp`). The Python GUI will warn you if it detects a file larger than 50 MB, as the Apps Script likely won't have enough memory to handle it.
* **Timeouts:** The Apps Script execution limit is 6 minutes. Extremely slow source servers might cause the script to time out before the file finishes transferring.
* **Direct Links Only:** The provided URL must be a direct file link (it should immediately start a download when pasted into a browser) and publicly accessible. Pages that require a login or clicking are not supported.

---

## 📝 License

This project is open-source and available under the MIT License.
