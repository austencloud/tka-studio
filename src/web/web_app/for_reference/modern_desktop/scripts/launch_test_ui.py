#!/usr/bin/env python3
"""
Simple launcher for the Image Export Test UI
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main():
    """Launch the Image Export Test UI"""
    script_dir = Path(__file__).parent
    ui_script = script_dir / "image_export_test_ui.py"

    if not ui_script.exists():
        print(f"❌ UI script not found: {ui_script}")
        return 1

    print("🚀 Launching Image Export Test UI...")
    print(f"📁 Script location: {ui_script}")
    print()
    print("Features:")
    print("  • Real-time image rendering with auto-refresh")
    print("  • Multiple preset sequences (1, 2, 4, 8 beats)")
    print("  • Customizable export options")
    print("  • JSON sequence editor")
    print("  • Image save functionality")
    print("  • Responsive UI with progress indicators")
    print()

    try:
        # Launch the UI
        subprocess.run([sys.executable, str(ui_script)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch UI: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n👋 UI closed by user")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
