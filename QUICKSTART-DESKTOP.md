# 🚀 Quick Start - Desktop App

## Step 1: Install Desktop Dependencies

```bash
pip install pywebview pythonnet
```

## Step 2: Build Your Angular Frontend

```bash
cd frontend
ng build --configuration production
cd ..
```

## Step 3: Run the App

### Option A: Double-click
Just double-click **`TaskManager.bat`** in Windows Explorer

### Option B: Command line
```bash
python launch_desktop.py
```

## Step 4: Create Desktop Shortcut (Optional)

```powershell
powershell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1
```

---

## ✅ That's it!

Your app will:
1. ✅ Start the backend server automatically
2. ✅ Open in a native desktop window
3. ✅ Look like a professional desktop application (no browser UI)
4. ✅ Close everything when you close the window

---

## 🔥 Pro Tip

After creating the desktop shortcut, you can:
- Pin it to taskbar
- Add it to Start Menu
- Launch it like any other desktop app!

---

## ⚠️ Troubleshooting

**Frontend not found?**
- Make sure you ran `ng build` in the frontend folder
- Check that `frontend/dist/` exists

**PyWebView error?**
- Run: `pip install pywebview pythonnet`

**Port already in use?**
- Stop any other app running on port 8000
- Or change the port in `launch_desktop.py`

