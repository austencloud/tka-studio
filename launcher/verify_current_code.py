#!/usr/bin/env python3
"""
Verify the current state of the application launch service.
"""

import sys
from pathlib import Path

# Add launcher to path
launcher_path = Path(__file__).parent
if str(launcher_path) not in sys.path:
    sys.path.insert(0, str(launcher_path))


def verify_current_code():
    """Verify what's actually in the current application launch service."""
    print("🔍 Verifying current application launch service code...")

    # Read the file directly
    service_file = launcher_path / "services" / "application_launch_service.py"

    with open(service_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for old vs new log messages
    old_message = (
        "DEBUG MODE: Launching {app.title} with direct import (debugger will follow)"
    )
    new_message = "DEBUG MODE: Launching {app.title} with debugpy subprocess (debugger will attach)"

    print(f"📄 File size: {len(content)} characters")
    print(f"🔍 Contains old message: {old_message in content}")
    print(f"🔍 Contains new message: {new_message in content}")

    # Check for other indicators
    print(f"🔍 Contains 'QTimer': {'QTimer' in content}")
    print(f"🔍 Contains 'launch_delayed': {'launch_delayed' in content}")
    print(f"🔍 Contains '_launch_tka_direct': {'_launch_tka_direct' in content}")
    print(
        f"🔍 Contains '_launch_tka_with_debugpy': {'_launch_tka_with_debugpy' in content}"
    )
    print(f"🔍 Contains 'debugpy subprocess': {'debugpy subprocess' in content}")

    # Check for the specific log messages that appear in the user's output
    problematic_messages = [
        "Direct launching TKA Desktop (Modern) in debug mode...",
        "scheduled for direct launch with debugger attached",
        "Loading main.py from:",
        "Setting up Python paths for desktop application...",
    ]

    print(f"\n🔍 Checking for problematic log messages:")
    for msg in problematic_messages:
        found = msg in content
        print(f"   '{msg}': {found}")
        if found:
            print("   ❌ This suggests old code is still present!")

    # Show the actual debug mode log message
    import re

    debug_mode_pattern = r'logger\.info\(\s*f"🐛 DEBUG MODE:.*?"'
    matches = re.findall(debug_mode_pattern, content, re.MULTILINE | re.DOTALL)

    print(f"\n🔍 Found debug mode log messages:")
    for i, match in enumerate(matches):
        print(f"   {i+1}: {match}")


if __name__ == "__main__":
    verify_current_code()
