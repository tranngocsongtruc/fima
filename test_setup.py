#!/usr/bin/env python3
"""
Quick setup test script
Run this to verify your installation is working
"""

import sys
from pathlib import Path

print("=" * 60)
print("Smart File Organizer - Setup Test")
print("=" * 60)
print()

# Test 1: Python version
print("1. Checking Python version...")
if sys.version_info >= (3, 10):
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}")
else:
    print(f"   ❌ Python {sys.version_info.major}.{sys.version_info.minor} (need 3.10+)")
    sys.exit(1)

# Test 2: Environment file
print("\n2. Checking .env file...")
env_file = Path(".env")
if env_file.exists():
    print("   ✅ .env file exists")
    
    # Check for API keys
    with open(env_file) as f:
        content = f.read()
        
    has_groq = "GROQ_API_KEY=gsk_" in content
    has_claude = "ANTHROPIC_API_KEY=sk-ant-" in content
    
    if has_groq:
        print("   ✅ Groq API key configured")
    else:
        print("   ⚠️  Groq API key not configured (add to .env)")
    
    if has_claude:
        print("   ✅ Claude API key configured")
    else:
        print("   ⚠️  Claude API key not configured (add to .env)")
else:
    print("   ❌ .env file not found")
    print("   → Run: cp .env.example .env")
    sys.exit(1)

# Test 3: Dependencies
print("\n3. Checking dependencies...")
try:
    import fastapi
    print("   ✅ FastAPI installed")
except ImportError:
    print("   ❌ FastAPI not installed")
    print("   → Run: pip install -r requirements.txt")

try:
    import groq
    print("   ✅ Groq SDK installed")
except ImportError:
    print("   ❌ Groq SDK not installed")
    print("   → Run: pip install -r requirements.txt")

try:
    import anthropic
    print("   ✅ Anthropic SDK installed")
except ImportError:
    print("   ❌ Anthropic SDK not installed")
    print("   → Run: pip install -r requirements.txt")

try:
    from watchdog.observers import Observer
    print("   ✅ Watchdog installed")
except ImportError:
    print("   ❌ Watchdog not installed")
    print("   → Run: pip install -r requirements.txt")

# Test 4: API Keys validation
print("\n4. Validating API keys...")
try:
    sys.path.insert(0, str(Path(__file__).parent / "backend"))
    from config import validate_api_keys
    
    if validate_api_keys():
        print("   ✅ All API keys valid")
    else:
        print("   ⚠️  Some API keys missing or invalid")
        print("   → Check your .env file")
except Exception as e:
    print(f"   ⚠️  Could not validate: {e}")

# Test 5: Directories
print("\n5. Checking directories...")
downloads = Path.home() / "Downloads"
if downloads.exists():
    print(f"   ✅ Downloads folder: {downloads}")
else:
    print(f"   ⚠️  Downloads folder not found")

docs = Path.home() / "Documents"
if docs.exists():
    print(f"   ✅ Documents folder: {docs}")
else:
    print(f"   ⚠️  Documents folder not found")

# Summary
print("\n" + "=" * 60)
print("Setup Test Complete!")
print("=" * 60)
print("\nNext steps:")
print("1. If any tests failed, fix them first")
print("2. Run: ./start.sh")
print("3. Open: http://127.0.0.1:8000")
print("\nHappy hacking! 🚀")
print()
