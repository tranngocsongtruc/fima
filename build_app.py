#!/usr/bin/env python3
"""
Build script to create a native macOS application bundle
This creates a downloadable .app that users can run directly
"""
import os
import shutil
import subprocess
from pathlib import Path

def create_app_bundle():
    """Create macOS .app bundle structure"""
    
    app_name = "SmartFileOrganizer"
    app_bundle = f"{app_name}.app"
    
    # Create .app directory structure
    contents = Path(app_bundle) / "Contents"
    macos = contents / "MacOS"
    resources = contents / "Resources"
    
    # Clean and create directories
    if Path(app_bundle).exists():
        shutil.rmtree(app_bundle)
    
    macos.mkdir(parents=True, exist_ok=True)
    resources.mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Created {app_bundle} structure")
    
    # Copy backend code
    shutil.copytree("backend", resources / "backend")
    shutil.copytree("frontend", resources / "frontend")
    
    # Copy requirements
    shutil.copy("requirements-core.txt", resources / "requirements.txt")
    shutil.copy(".env.example", resources / ".env.example")
    
    print("✅ Copied application files")
    
    # Create launcher script
    launcher_script = macos / app_name
    with open(launcher_script, 'w') as f:
        f.write('''#!/bin/bash
# SmartFileOrganizer Launcher

# Get the directory where the app is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RESOURCES="$DIR/../Resources"

# Change to resources directory
cd "$RESOURCES"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 First launch - setting up environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Please configure your API keys."
    open -e .env.example
    exit 1
fi

# Launch the application
echo "🚀 Starting Smart File Organizer..."
python3 backend/main.py

# Keep terminal open
read -p "Press Enter to close..."
''')
    
    # Make launcher executable
    os.chmod(launcher_script, 0o755)
    
    print("✅ Created launcher script")
    
    # Create Info.plist
    info_plist = contents / "Info.plist"
    with open(info_plist, 'w') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>SmartFileOrganizer</string>
    <key>CFBundleIdentifier</key>
    <string>com.calhacks.smartfileorganizer</string>
    <key>CFBundleName</key>
    <string>Smart File Organizer</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>12.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
''')
    
    print("✅ Created Info.plist")
    
    # Create DMG for distribution
    print("\n📦 Creating DMG for distribution...")
    dmg_name = f"{app_name}.dmg"
    
    if Path(dmg_name).exists():
        os.remove(dmg_name)
    
    subprocess.run([
        "hdiutil", "create",
        "-volname", app_name,
        "-srcfolder", app_bundle,
        "-ov", "-format", "UDZO",
        dmg_name
    ])
    
    print(f"\n✅ Created {dmg_name}")
    print(f"\n🎉 Build complete!")
    print(f"\nUsers can download {dmg_name} and drag {app_bundle} to Applications")
    
    return app_bundle, dmg_name

if __name__ == "__main__":
    create_app_bundle()
