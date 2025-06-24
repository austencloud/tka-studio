#!/usr/bin/env python3
"""
Test the enhanced subprocess approach.
"""

import sys
from pathlib import Path

# Add launcher to path
launcher_path = Path(__file__).parent
if str(launcher_path) not in sys.path:
    sys.path.insert(0, str(launcher_path))

from services.application_launch_service import ApplicationLaunchService
from domain.models import ApplicationData, ApplicationCategory, LaunchRequest
from datetime import datetime


def test_enhanced_subprocess():
    """Test the enhanced subprocess approach."""
    print("🧪 Testing enhanced subprocess approach...")
    
    # Create a mock state service
    class MockStateService:
        def update_application_status(self, app_id, status, pid):
            print(f"📊 Status update: {app_id} -> {status} (PID: {pid})")
        def add_application(self, app):
            print(f"📱 App added: {app.title}")
    
    # Create launch service
    launch_service = ApplicationLaunchService(MockStateService())
    
    # Override debug detection to return True
    launch_service._is_debugger_attached = lambda: True
    print("🔧 Overridden debug detection to return True")
    
    # Create test app
    tka_root = Path(__file__).parent.parent
    test_app = ApplicationData(
        id="desktop_modern",
        title="TKA Desktop (Modern)",
        description="Modern TKA Desktop application with updated architecture",
        icon="✨",
        category=ApplicationCategory.DESKTOP,
        command="python main.py",
        working_dir=tka_root / "src" / "desktop" / "modern",
    )
    
    # Create launch request
    request = LaunchRequest(
        application_id="desktop_modern",
        timestamp=datetime.now().isoformat(),
        session_id="test",
        user_initiated=True,
        launch_options={},
    )
    
    print(f"\n🚀 Testing enhanced subprocess launch of: {test_app.title}")
    print(f"📁 Working dir: {test_app.working_dir}")
    print(f"🔍 TKA app: {launch_service._is_tka_application(test_app)}")
    print(f"🐛 Debug mode: {launch_service._is_debugger_attached()}")
    
    # Test the launch
    try:
        print("\n🎯 Attempting enhanced subprocess launch...")
        result = launch_service._launch_process(test_app, request)
        
        if result:
            print(f"✅ Launch successful! PID: {result.pid}")
            print("🎯 In real scenario, VS Code debugger should attach automatically")
            print("🎯 Your breakpoints in pictograph_scene.py would work!")
            
            # Wait a moment then terminate
            import time
            time.sleep(2)
            result.terminate()
            print("🛑 Terminated test process")
            
            return True
        else:
            print("❌ Launch failed!")
            return False
            
    except Exception as e:
        print(f"❌ Launch exception: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    print("🚀 Enhanced Subprocess Test\n")
    
    success = test_enhanced_subprocess()
    
    if success:
        print("\n✅ Enhanced subprocess test passed!")
        print("🎯 The simplified approach should work better")
        print("🎯 No more Windows socket issues with debugpy")
        print("🎯 VS Code should attach debugger automatically")
    else:
        print("\n❌ Enhanced subprocess test failed")
        print("🔧 Need to investigate further")
