#!/usr/bin/env python3
"""
Quick test script to verify the horizontal launcher setup.
"""

import sys
from pathlib import Path

# Add launcher directory to path
launcher_dir = Path(__file__).parent
sys.path.insert(0, str(launcher_dir))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        print("Testing imports...")
        
        print("✓ Testing launcher_config...")
        from config.config.launcher_config import LauncherConfig
        
        print("✓ Testing tka_integration...")
        from tka_integration import TKAIntegrationService
        
        print("✓ Testing horizontal_launcher...")
        from horizontal_launcher import TKAHorizontalLauncher
        
        print("✓ Testing unified_launcher...")
        from unified_launcher import TKAUnifiedLauncher
        
        print("✓ Testing main launcher...")
        from main import TKAHorizontalLauncherApp
        
        print("🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_config():
    """Test the configuration system."""
    try:
        print("\nTesting configuration...")
        from config.config.launcher_config import LauncherConfig
        
        config = LauncherConfig()
        print(f"✓ Default mode: {config.get_window_mode()}")
        print(f"✓ Launcher type: {config.get_launcher_type()}")
        print(f"✓ Taskbar overlay: {config.is_taskbar_overlay_enabled()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing TKA Horizontal Launcher Setup")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_config()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Your horizontal launcher is ready.")
        print("\n💡 To start the launcher:")
        print("   python main.py")
        print("   or")
        print("   double-click start_horizontal_launcher.bat")
    else:
        print("❌ Some tests failed. Check the error messages above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
