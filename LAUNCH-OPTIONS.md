# Task Manager Launch Options

## 🚀 Different Ways to Launch

### Option 1: Silent Mode (Recommended) ⭐
**No console window** - Launches like a native app

Double-click: `TaskManager-Silent.vbs`

**Features:**
- ✅ No console window in background
- ✅ Clean desktop app experience
- ✅ Uses custom icon
- ✅ Minimal logging output

---

### Option 2: Batch File (With Console)
**Shows console window** - Good for debugging

Double-click: `TaskManager.bat`

**Features:**
- ✅ See startup messages
- ✅ Good for troubleshooting
- ✅ Shows progress indicators
- ⚠️ Console window stays open

---

### Option 3: Python Direct
**Terminal/Command Line** - For developers

```bash
python launch_desktop.py
```

**Features:**
- ✅ Full control from terminal
- ✅ Easy to restart/debug
- ✅ Can see all output

---

## 📌 Desktop Shortcut

Create a desktop shortcut (uses silent mode if available):

```powershell
powershell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1
```

This creates a **"Task Manager"** shortcut on your desktop with:
- ✅ Custom icon
- ✅ Silent launch (no console)
- ✅ Professional appearance

---

## 🔇 Logging Levels

The application now uses **minimal logging**:

- **SQLAlchemy queries**: Hidden ✅
- **Library logs**: Only warnings/errors ✅
- **App status**: Clean, concise messages ✅

### What You'll See Now:

```
==================================================
🚀 Task Manager - Desktop Application
==================================================

⏳ Starting backend server... ✅

==================================================
🚀 Task Manager is running!
==================================================
Close the window to exit the application
```

Much cleaner! 🎉

---

## 💡 Tips

1. **First Launch**: Use `TaskManager.bat` to verify everything works
2. **Daily Use**: Use `TaskManager-Silent.vbs` or desktop shortcut
3. **Debugging**: Use `python launch_desktop.py` in terminal

---

## 🎨 Custom Icon

Your Task Manager now has a custom purple checklist icon!

- **Window icon**: ✅ (taskbar & title bar)
- **Desktop shortcut**: ✅
- **Alt+Tab**: ✅

To change the icon, replace `taskmanager.ico` or run:
```bash
python create_icon.py
```

Enjoy your clean, professional Task Manager! 🚀

