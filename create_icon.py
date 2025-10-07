"""
Create a custom icon for Task Manager
Generates a simple icon with a checklist emoji/design
"""

import os

def create_simple_icon():
    """
    Create a simple .ico file for Task Manager
    Uses PIL (Pillow) to create the icon
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("❌ Pillow not installed!")
        print("   Install it with: pip install Pillow")
        return False
    
    # Create a 256x256 image with transparent background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a rounded rectangle background (gradient-like)
    # Purple gradient colors
    bg_color = (102, 126, 234, 255)  # #667eea
    draw.rounded_rectangle([(20, 20), (236, 236)], radius=40, fill=bg_color)
    
    # Draw checklist lines (white)
    line_color = (255, 255, 255, 255)
    line_width = 8
    
    # Checkmarks (3 items)
    check_positions = [70, 120, 170]
    for y in check_positions:
        # Checkbox
        draw.rounded_rectangle([(50, y), (85, y + 35)], radius=5, outline=line_color, width=3)
        # Checkmark inside
        draw.line([(55, y + 15), (65, y + 25), (80, y + 10)], fill=line_color, width=4)
        # Task line
        draw.rounded_rectangle([(100, y + 10), (200, y + 25)], radius=3, fill=line_color)
    
    # Save as .ico file with multiple sizes
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save('taskmanager.ico', format='ICO', sizes=icon_sizes)
    
    print("✅ Icon created successfully: taskmanager.ico")
    return True


def download_icon_alternative():
    """
    Alternative: Download a free icon from the internet
    """
    print("\n📥 Alternative: Download a free icon")
    print("   1. Visit: https://icons8.com/icons/set/task-manager")
    print("   2. Or: https://www.flaticon.com/search?word=checklist")
    print("   3. Download as .ico format (256x256 recommended)")
    print("   4. Save as 'taskmanager.ico' in this directory")
    print()


if __name__ == "__main__":
    print("🎨 Creating Task Manager Icon...")
    print("=" * 50)
    
    if not create_simple_icon():
        download_icon_alternative()
        print("\n⚠️  After getting an icon, run this script again or")
        print("   manually save it as 'taskmanager.ico' in the project folder")
    else:
        print("\n✅ Icon is ready!")
        print("   File: taskmanager.ico")
        print("\n💡 The icon will be used when you launch the desktop app")

