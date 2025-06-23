#!/usr/bin/env python3
"""
Test script to verify debug detection works correctly.
"""

import sys
from pathlib import Path

# Add launcher to path
launcher_path = Path(__file__).parent
if str(launcher_path) not in sys.path:
    sys.path.insert(0, str(launcher_path))

from services.application_launch_service import ApplicationLaunchService
from domain.models import ApplicationData, ApplicationCategory


def test_debug_detection():
    """Test if debug detection works."""
    print("🧪 Testing debug detection...")
    
    # Create a mock state service
    class MockStateService:
        def update_application_status(self, app_id, status, pid):
            pass
        def add_application(self, app):
            pass
    
    # Create launch service
    launch_service = ApplicationLaunchService(MockStateService())
    
    # Test debug detection
    debug_mode = launch_service._is_debugger_attached()
    print(f"🐛 Debug mode detected: {debug_mode}")
    
    if debug_mode:
        print("✅ Debugger is attached - TKA apps will launch directly!")
        print("🎯 Your breakpoints will work in pictograph_scene.py")
    else:
        print("ℹ️ No debugger detected - TKA apps will use subprocess")
        print("💡 Run this with F5 in VS Code to test debug mode")
    
    # Test TKA app detection
    test_apps = [
        ApplicationData(
            id="desktop_modern",
            title="TKA Desktop Modern",
            description="Test app",
            icon="✨",
            category=ApplicationCategory.DESKTOP,
            command="python main.py --modern",
            working_dir=Path.cwd(),
        ),
        ApplicationData(
            id="some_other_app",
            title="Other App",
            description="Non-TKA app",
            icon="🔧",
            category=ApplicationCategory.DEVELOPMENT,
            command="python other.py",
            working_dir=Path.cwd(),
        )
    ]
    
    for app in test_apps:
        is_tka = launch_service._is_tka_application(app)
        print(f"📱 {app.title}: TKA app = {is_tka}")
    
    return debug_mode


if __name__ == "__main__":
    test_debug_detection()
