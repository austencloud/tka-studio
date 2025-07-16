#!/usr/bin/env python3
"""
Minimal launcher test to isolate the src path issue.
"""

import os
import sys
from pathlib import Path

print("🔥 MINIMAL LAUNCHER TEST STARTING")
print(f"📁 Working directory: {os.getcwd()}")
print(f"🛤️ Python path entries:")
for i, path in enumerate(sys.path[:5]):
    print(f"   {i+1}. {path}")

print("\n🧪 Testing imports step by step...")

try:
    print("1. Testing basic Python imports...")
    import logging
    from pathlib import Path

    print("   ✅ Basic imports OK")

    print("2. Testing PyQt6...")
    from PyQt6.QtWidgets import QApplication

    print("   ✅ PyQt6 OK")

    print("3. Testing domain models...")
    from domain.models import LauncherState

    print("   ✅ Domain models OK")

    print("4. Testing core interfaces...")
    from core.interfaces import IApplicationService

    print("   ✅ Core interfaces OK")

    print("5. Testing DI integration...")
    from core.di_integration import LauncherDIContainer

    print("   ✅ DI integration OK")

    print("6. Testing TKA integration...")
    from integration.tka_integration import TKAIntegrationService

    print("   ✅ TKA integration OK")

    print("7. Testing launcher window...")
    from ui.windows.launcher_window import TKALauncherWindow

    print("   ✅ Launcher window OK")

    print("\n🎉 ALL IMPORTS SUCCESSFUL!")
    print("🚀 The launcher should work now!")

except Exception as e:
    print(f"\n❌ Import failed at step: {e}")
    import traceback

    traceback.print_exc()

print("\n🏁 Minimal test complete!")
