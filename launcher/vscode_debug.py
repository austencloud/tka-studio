#!/usr/bin/env python3
"""
VS Code workspace debugging script.
"""

import os
import sys
from pathlib import Path

print("🔍 VS CODE WORKSPACE DEBUG")
print("=" * 50)
print(f"📁 Current working directory: {os.getcwd()}")
print(f"🐍 Python executable: {sys.executable}")
print(f"📄 Script file: {__file__}")
print(f"📄 Script resolved: {Path(__file__).resolve()}")
print(f"📁 Script parent: {Path(__file__).parent}")
print(f"📁 Script parent resolved: {Path(__file__).parent.resolve()}")

print(f"\n🛤️ Python path (first 3):")
for i, path in enumerate(sys.path[:3]):
    print(f"   {i+1}. {path}")

print(f"\n🔧 Environment:")
print(f"   PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"   VIRTUAL_ENV: {os.environ.get('VIRTUAL_ENV', 'Not set')}")

print(f"\n🎯 Expected paths:")
print(f"   Workspace should be: F:\\CODE\\TKA")
print(f"   Launcher dir should be: F:\\CODE\\TKA\\launcher")
print(f"   This script should be: F:\\CODE\\TKA\\launcher\\vscode_debug.py")

print("\n✅ If you see this, F5 is working and running the correct file!")

# Test if we can import launcher modules
try:
    print("\n🧪 Testing launcher imports...")
    from desktop.modern.domain.models import LauncherState

    print("✅ domain.models imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback

    traceback.print_exc()

if __name__ == "__main__":
    print("\n🎯 __main__ block executed successfully!")
