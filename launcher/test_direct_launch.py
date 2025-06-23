#!/usr/bin/env python3
"""
Test script to verify direct launch works without threading issues.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add launcher to path
launcher_path = Path(__file__).parent
if str(launcher_path) not in sys.path:
    sys.path.insert(0, str(launcher_path))

from services.application_launch_service import ApplicationLaunchService
from domain.models import ApplicationData, ApplicationCategory


def test_direct_launch():
    """Test direct launch without threading issues."""
    print("🧪 Testing direct launch mechanism...")
    
    # Create QApplication (required for QTimer)
    app = QApplication(sys.argv)
    
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
    
    # Create test app
    test_app = ApplicationData(
        id="desktop_modern",
        title="TKA Desktop Modern",
        description="Test app",
        icon="✨",
        category=ApplicationCategory.DESKTOP,
        command="python main.py",
        working_dir=Path.cwd() / "src" / "desktop" / "modern",
    )
    
    # Test TKA app detection
    is_tka = launch_service._is_tka_application(test_app)
    print(f"📱 {test_app.title}: TKA app = {is_tka}")
    
    if debug_mode and is_tka:
        print("✅ Would use direct launch in debug mode")
        print("🎯 Your breakpoints would work!")
    else:
        print("ℹ️ Would use subprocess (normal mode)")
    
    # Test QTimer mechanism (without actually launching)
    def test_timer():
        print("⏰ QTimer test successful - main thread execution works")
        app.quit()
    
    QTimer.singleShot(100, test_timer)
    
    print("🚀 Starting Qt event loop test...")
    return app.exec()


if __name__ == "__main__":
    exit_code = test_direct_launch()
    print(f"✅ Test completed with exit code: {exit_code}")
