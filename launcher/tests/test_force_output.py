#!/usr/bin/env python3
"""
Force-output version of launcher main for debugging.
"""

import os
import sys

# Force unbuffered output
sys.stdout.flush()
sys.stderr.flush()


def force_print(msg):
    """Print with forced flushing."""
    print(msg)
    sys.stdout.flush()


def main():
    force_print("🚨 STARTING FORCE-OUTPUT LAUNCHER TEST")
    force_print(f"📁 Working directory: {os.getcwd()}")
    force_print(f"🐍 Python: {sys.executable}")

    try:
        force_print("🧪 Testing basic imports...")
        import logging

        force_print("✅ logging imported")

        from pathlib import Path

        force_print("✅ pathlib imported")

        force_print("🧪 Testing PyQt6...")
        from PyQt6.QtWidgets import QApplication

        force_print("✅ PyQt6.QtWidgets imported")

        from PyQt6.QtCore import Qt

        force_print("✅ PyQt6.QtCore imported")

        force_print("🧪 Creating QApplication...")
        app = QApplication([])
        force_print("✅ QApplication created successfully!")

        force_print("🧪 Testing launcher imports...")
        from domain.models import LauncherState

        force_print("✅ domain.models imported")

        from core.interfaces import IApplicationService

        force_print("✅ core.interfaces imported")

        from integration.tka_integration import TKAIntegrationService

        force_print("✅ integration.tka_integration imported")

        force_print("🎉 ALL IMPORTS SUCCESSFUL!")
        force_print("🚨 TEST COMPLETE - NO ISSUES FOUND")

        return 0

    except Exception as e:
        force_print(f"❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        return 1


if __name__ == "__main__":
    force_print("🚨 FORCE-OUTPUT TEST STARTING...")
    result = main()
    force_print(f"🚨 FORCE-OUTPUT TEST FINISHED WITH CODE: {result}")
    sys.exit(result)
