"""
Setup Verification Script
Run this to check if your desktop app is ready to launch
"""

import sys
from pathlib import Path

print("\n" + "=" * 60)
print("Task Manager Desktop - Setup Verification")
print("=" * 60 + "\n")

all_checks_passed = True

# Check 1: Python version
print("1. Checking Python version...")
python_version = sys.version_info
if python_version.major == 3 and python_version.minor >= 11:
    print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} (OK)")
else:
    print(f"   ❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} (Need 3.11+)")
    all_checks_passed = False

# Check 2: Required packages
print("\n2. Checking Python packages...")
required_packages = [
    ('fastapi', 'FastAPI'),
    ('uvicorn', 'Uvicorn'),
    ('sqlalchemy', 'SQLAlchemy'),
    ('pydantic', 'Pydantic'),
]

for package, name in required_packages:
    try:
        __import__(package)
        print(f"   ✅ {name}")
    except ImportError:
        print(f"   ❌ {name} (run: pip install -r requirements.txt)")
        all_checks_passed = False

# Check 3: Desktop packages
print("\n3. Checking desktop packages...")
try:
    import webview
    print(f"   ✅ PyWebView")
except ImportError:
    print(f"   ❌ PyWebView (run: pip install pywebview)")
    all_checks_passed = False

try:
    import clr
    print(f"   ✅ Pythonnet")
except ImportError:
    print(f"   ⚠️  Pythonnet (run: pip install pythonnet)")
    print(f"      Note: Optional but recommended for Windows")

# Check 4: Frontend build
print("\n4. Checking Angular frontend...")
frontend_paths = [
    Path(__file__).parent / "frontend" / "dist" / "browser" / "index.html",
    Path(__file__).parent / "frontend" / "dist" / "index.html",
    Path("D:/Angular/task-manager-portal/dist/task-manager-portal/browser/index.html"),
    Path("D:/Angular/task-manager-portal/dist/task-manager-portal/index.html"),
    Path("D:/Angular/task-manager-portal/dist/browser/index.html"),
    Path("D:/Angular/task-manager-portal/dist/index.html"),
]

frontend_found = False
for path in frontend_paths:
    if path.exists():
        print(f"   ✅ Frontend built at: {path.parent}")
        frontend_found = True
        break

if not frontend_found:
    print(f"   ❌ Frontend not built")
    print(f"      Run: cd D:\\Angular\\task-manager-portal && ng build --configuration production")
    all_checks_passed = False

# Check 5: Required files
print("\n5. Checking required files...")
required_files = [
    'app/main.py',
    'launch_desktop.py',
    'TaskManager.bat',
    'requirements.txt'
]

for file in required_files:
    file_path = Path(__file__).parent / file
    if file_path.exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} (missing)")
        all_checks_passed = False

# Check 6: Database configuration
print("\n6. Checking configuration...")
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    print(f"   ✅ .env file exists")
else:
    print(f"   ⚠️  .env file not found (using defaults)")
    print(f"      Copy env.example to .env and configure")

# Final result
print("\n" + "=" * 60)
if all_checks_passed:
    print("✅ ALL CHECKS PASSED!")
    print("=" * 60)
    print("\nYou're ready to launch the desktop app!")
    print("\nRun one of these commands:")
    print("  • Double-click: TaskManager.bat")
    print("  • Command line: python launch_desktop.py")
    print("\n")
else:
    print("❌ SOME CHECKS FAILED")
    print("=" * 60)
    print("\nPlease fix the issues above before running the app.")
    print("\nQuick fixes:")
    print("  • Install dependencies: pip install -r requirements.txt")
    print("  • Install desktop: pip install pywebview pythonnet")
    print("  • Build frontend: cd frontend && ng build --configuration production")
    print("\n")

input("Press Enter to exit...")

