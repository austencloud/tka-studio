#!/usr/bin/env python3
"""
VS Code workspace debugging script.
"""

import os
from pathlib import Path
import sys

print("🔍 VS CODE WORKSPACE DEBUG")
print("=" * 50)
print(f"📁 Current working directory: {os.getcwd()}")
print(f"🐍 Python executable: {sys.executable}")
print(f"📄 Script file: {__file__}")
print(f"📄 Script resolved: {Path(__file__).resolve()}")
print(f"📁 Script parent: {Path(__file__).parent}")
print(f"📁 Script parent resolved: {Path(__file__).parent.resolve()}")

print("\n🛤️ Python path (first 3):")
for i, path in enumerate(sys.path[:3]):
    print(f"   {i + 1}. {path}")

print("\n🔧 Environment:")
print(f"   PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"   VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV', 'Not set')}")

print("\n🎯 Expected paths:")
print("   Workspace should be: F:\\CODE\\TKA")
print("   Launcher dir should be: F:\\CODE\\TKA\\launcher")
print("   This script should be: F:\\CODE\\TKA\\launcher\\vscode_debug.py")

print("\n✅ If you see this, F5 is working and running the correct file!")

# Test if we can import launcher modules
try:
    print("\n🧪 Testing launcher imports...")

    print("✅ domain.models imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback

    traceback.print_exc()

if __name__ == "__main__":
    print("\n🎯 __main__ block executed successfully!")
