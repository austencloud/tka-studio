#!/usr/bin/env python3
"""
Quick test script to verify the horizontal launcher setup.
"""

import sys
from pathlib import Path

# Add launcher directory to path
launcher_dir = Path(__file__).parent.parent
sys.path.insert(0, str(launcher_dir))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        print("Testing imports...")
        
        print("✓ Testing settings...")
        from config.settings import SettingsManager, LauncherSettings
        
        print("✓ Testing tka_integration...")
        from integration.tka_integration import TKAIntegrationService
        
        print("✓ Testing main launcher...")
        from main import TKAModernLauncherApp
        
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
        from config.settings import SettingsManager
        
        # Create settings manager (won't save to file in test)
        settings = SettingsManager()
        print(f"✓ Default mode: {settings.get('launch_mode')}")
        print(f"✓ Window width: {settings.get('window_width')}")
        print(f"✓ Window height: {settings.get('window_height')}")
        print(f"✓ Theme: {settings.get('theme')}")
        print(f"✓ Dock position: {settings.get('dock_position')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test error: {e}")
        return False

def test_integration():
    """Test TKA integration service."""
    try:
        print("\nTesting TKA integration...")
        from integration.tka_integration import TKAIntegrationService
        
        # Create integration service
        integration = TKAIntegrationService()
        print("✓ TKA integration service created")
        
        # Test getting applications
        apps = integration.get_applications()
        print(f"✓ Found {len(apps)} applications")
        
        # List application names
        for app in apps[:3]:  # Show first 3 apps
            print(f"   - {app.title}")
        
        # Test cleanup
        integration.cleanup()
        print("✓ Integration cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing TKA Modern Launcher Setup")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_config()
    success &= test_integration()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Your launcher is ready.")
        print("\n💡 To start the launcher:")
        print("   python main.py")
    else:
        print("❌ Some tests failed. Check the error messages above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
