# 📥 Google Drive Relay Downloader

A desktop GUI tool that downloads any file (from any public URL) and saves it directly to your **Google Drive** – using a Google Apps Script as a relay.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Apps Script](https://img.shields.io/badge/Google-AppsScript-yellow)

## 🚀 How It Works

1. You provide a **file URL** (e.g., `https://example.com/file.pdf`)  
2. The Python GUI sends the URL + desired filename to your **Google Apps Script web app**  
3. The Apps Script fetches the file and saves it into your **Google Drive folder**  
4. The GUI shows you the Drive file URL

> ⚡ Bypasses local download – the file goes directly from source to Drive.

## 🛠️ Setup Instructions

### 1. Deploy the Google Apps Script

- Open [script.google.com](https://script.google.com) and create a new project.
- Replace the default code with the content of [`ScriptToDeploy.gs`](ScriptToDeploy.gs).
- **Modify the folder ID** inside the script:  
  `const folderId = 'YOUR_DRIVE_FOLDER_ID';`  
  (Find your folder ID in its Drive URL: `https://drive.google.com/drive/folders/THIS_IS_THE_ID`)
- Deploy as a **Web App**:
  - Execute as: **Me**  
  - Who has access: **Anyone** (or “Anyone with link” – the tool sends public files)
  - Click **Deploy** → **New deployment** → **Web app**  
  - Copy the **deployment URL** (looks like `https://script.google.com/macros/s/.../exec`)

### 2. Configure the Python GUI

- Install Python 3.7+ and required library:  
  `pip install requests`
- Edit `relay_config.json` and paste your Apps Script URL:  
  ```json
  {
    "script_url": "https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec",
    "folder_id": ""
  }
