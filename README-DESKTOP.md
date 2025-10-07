# Task Manager - Desktop Application

This is a native desktop application that combines your FastAPI backend with Angular frontend into a single-window desktop app.

## 🚀 Features

- **Native Desktop Window** - Runs like a real desktop application (no browser UI)
- **Single Click Launch** - Just double-click the icon
- **Auto-Start Backend** - Backend server starts automatically
- **Clean Interface** - No address bar, tabs, or browser clutter
- **Windows Optimized** - Built specifically for Windows 10/11

---

## 📋 Prerequisites

1. **Python 3.11+** installed and in PATH
2. **Node.js & Angular CLI** (for building frontend)
3. **PostgreSQL** (or SQLite for local development)

---

## 🛠️ Setup Instructions

### Step 1: Install Python Dependencies

```bash
# Install backend dependencies
pip install -r requirements.txt

# Install desktop dependencies
pip install -r requirements-desktop.txt
```

Or let the batch file do it automatically!

---

### Step 2: Build Angular Frontend

```bash
# Navigate to your Angular project
cd frontend

# Build for production
ng build --configuration production

# The build output will be in frontend/dist/
```

**Important:** Make sure your Angular project is in a folder named `frontend` inside this project.

---

### Step 3: Create Desktop Shortcut (Optional)

Run this in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1
```

This creates a shortcut on your desktop!

---

## 🎮 How to Run

### Option 1: Double-click the Batch File
Just double-click **`TaskManager.bat`** in Windows Explorer

### Option 2: Run from Command Line
```bash
python launch_desktop.py
```

### Option 3: Use Desktop Shortcut
Double-click the **Task Manager** icon on your desktop (after creating shortcut)

---

## 📁 Project Structure

```
Task_Manager/
├── app/                      # FastAPI backend
│   ├── api/
│   ├── models/
│   ├── services/
│   └── main.py              # Updated to serve Angular
├── frontend/                 # Angular source code
│   ├── src/
│   └── dist/                # Built Angular app (after ng build)
├── launch_desktop.py        # Desktop launcher (PyWebView)
├── TaskManager.bat          # Windows launcher
├── requirements.txt         # Backend dependencies
├── requirements-desktop.txt # Desktop dependencies
└── create_desktop_shortcut.ps1  # Shortcut creator
```

---

## 🔧 Troubleshooting

### "Frontend not built" error
**Solution:** Build your Angular app first
```bash
cd frontend
ng build --configuration production
```

### PyWebView not installed
**Solution:** Install desktop dependencies
```bash
pip install pywebview pythonnet
```

### Port 8000 already in use
**Solution:** Stop other applications using port 8000, or change the port in `launch_desktop.py`

### Window opens but shows error
**Solution:** Check that:
1. Angular is built (`frontend/dist/` exists)
2. Backend dependencies are installed
3. Database is configured in `.env` file

---

## 🎨 Customization

### Change Window Size
Edit `launch_desktop.py`:
```python
window = webview.create_window(
    title='Task Manager',
    url='http://127.0.0.1:8000',
    width=1280,  # Change this
    height=800,  # Change this
    ...
)
```

### Change Port
Edit `launch_desktop.py` (change all instances of 8000 to your port)

### Add Custom Icon
1. Create or download an `.ico` file
2. Name it `app_icon.ico`
3. Place it in the project root
4. Run `create_desktop_shortcut.ps1` again

---

## 📦 Creating a Standalone EXE (Advanced)

Want to distribute your app without requiring Python installation?

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name="TaskManager" --icon=app_icon.ico launch_desktop.py
```

The `.exe` will be in the `dist/` folder.

---

## 🤝 Contributing

This is a personal project, but feel free to fork and customize!

---

## 📄 License

Your license here

---

## 🎉 Enjoy Your Desktop App!

You now have a professional desktop application that:
- ✅ Starts with one click
- ✅ Looks like a native app
- ✅ Combines backend and frontend seamlessly
- ✅ Runs entirely on your local machine

