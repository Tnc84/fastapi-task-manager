"""
Task Manager - Native Desktop Application
Uses PyWebView to create a native window experience
"""

import os
import sys
import time
import socket
import logging
import threading
import multiprocessing
from pathlib import Path

# Configure logging - only show warnings and errors from libraries
logging.basicConfig(
    level=logging.WARNING,
    format='%(message)s'
)
# But keep INFO level for our own app logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def is_port_in_use(port: int) -> bool:
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


def start_backend_server():
    """
    Start FastAPI backend server
    Runs in a separate process to avoid blocking
    """
    try:
        import uvicorn
        
        # Suppress uvicorn startup logs
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            log_level="error",  # Only show errors
            access_log=False
        )
    except Exception as e:
        logger.error(f"Failed to start backend server: {e}")
        sys.exit(1)


def wait_for_server(max_attempts=30):
    """
    Wait for the backend server to be ready
    Returns True if server is ready, False otherwise
    """
    print("⏳ Starting backend server...", end="", flush=True)
    
    for attempt in range(max_attempts):
        if is_port_in_use(8000):
            print(" ✅")
            return True
        time.sleep(0.5)
    
    print(" ❌ Failed!")
    logger.error("Backend server failed to start")
    return False


def check_frontend_exists():
    """Check if Angular frontend is built"""
    frontend_paths = [
        Path(__file__).parent / "frontend" / "dist" / "browser" / "index.html",
        Path(__file__).parent / "frontend" / "dist" / "index.html",
        Path("D:/Angular/task-manager-portal/dist/task-manager-portal/browser/index.html"),
        Path("D:/Angular/task-manager-portal/dist/task-manager-portal/index.html"),
        Path("D:/Angular/task-manager-portal/dist/browser/index.html"),
        Path("D:/Angular/task-manager-portal/dist/index.html"),
    ]
    
    for path in frontend_paths:
        if path.exists():
            return True
    
    print("⚠️  Frontend not built - API only mode")
    return False


def create_native_window():
    """
    Create native desktop window using PyWebView
    """
    try:
        import webview
    except ImportError:
        logger.error("❌ PyWebView not installed!")
        logger.error("   Install it with: pip install pywebview")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Check if custom icon exists
    icon_path = Path(__file__).parent / "taskmanager.ico"
    if not icon_path.exists():
        icon_path = None
    
    # Create the window (icon will be set in webview.start())
    window = webview.create_window(
        title='Task Manager',
        url='http://127.0.0.1:8000',
        width=1280,
        height=800,
        resizable=True,
        fullscreen=False,
        min_size=(800, 600),
        background_color='#FFFFFF',
        text_select=True
    )
    
    print("\n" + "=" * 50)
    print("🚀 Task Manager is running!")
    print("=" * 50)
    print("Close the window to exit the application\n")
    
    # Start the GUI event loop (blocking) with icon
    if icon_path:
        webview.start(icon=str(icon_path))
    else:
        webview.start()
    
    logger.info("Desktop window closed. Shutting down...")


def main():
    """Main entry point for the desktop application"""
    print("\n" + "=" * 50)
    print("🚀 Task Manager - Desktop Application")
    print("=" * 50 + "\n")
    
    # Check if frontend is built
    check_frontend_exists()
    
    # Check if backend is already running
    if is_port_in_use(8000):
        print("⚠️  Backend already running on port 8000")
        print("📱 Opening window...\n")
        create_native_window()
        return
    
    # Start backend server in separate process
    server_process = multiprocessing.Process(target=start_backend_server, daemon=True)
    server_process.start()
    
    # Wait for server to be ready
    if not wait_for_server():
        logger.error("Failed to start the application")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Small delay to ensure server is fully ready
    time.sleep(1)
    
    try:
        # Create and show native window
        create_native_window()
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
    finally:
        # Cleanup
        print("Shutting down...")
        if server_process.is_alive():
            server_process.terminate()
            server_process.join(timeout=5)
        print("✅ Closed\n")


if __name__ == "__main__":
    # Required for Windows multiprocessing
    multiprocessing.freeze_support()
    
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

