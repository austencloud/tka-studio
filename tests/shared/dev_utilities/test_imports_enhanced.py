#!/usr/bin/env python3
"""
Enhanced test script to validate all imports work correctly.
Run this from the project root to check if your configuration is working.
"""

import sys
import os

# Add project paths (same as in .pylintrc)
project_root = os.path.abspath(".")
launcher_path = os.path.join(project_root, "launcher")
modern_src_path = os.path.join(project_root, "src", "desktop", "modern", "src")

paths_to_add = [project_root, launcher_path, modern_src_path]
for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

print("🔍 Testing enhanced import resolution...")
print(f"Project root: {project_root}")
print(f"Launcher path: {launcher_path}")
print(f"Modern src path: {modern_src_path}")
print(f"Python path (first 5): {sys.path[:5]}")

def test_imports():
    """Test all the problematic imports."""
    errors = []
    
    # Test PyQt6 imports
    try:
        print("\n✅ Testing PyQt6 imports...")
        from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
        from PyQt6.QtCore import Qt, pyqtSignal
        from PyQt6.QtGui import QFont, QPixmap
        print("   ✓ PyQt6 imports successful")
    except ImportError as e:
        errors.append(f"PyQt6: {e}")
        print(f"   ❌ PyQt6 import failed: {e}")

    # Test launcher UI imports
    try:
        print("\n✅ Testing launcher ui.components import...")
        from ui.components import ReliableApplicationCard
        print("   ✓ ui.components import successful")
    except ImportError as e:
        errors.append(f"ui.components: {e}")
        print(f"   ❌ ui.components import failed: {e}")

    try:
        print("\n✅ Testing launcher ui.reliable_effects import...")
        from ui.reliable_effects import get_animation_manager
        print("   ✓ ui.reliable_effects import successful")
    except ImportError as e:
        errors.append(f"ui.reliable_effects: {e}")
        print(f"   ❌ ui.reliable_effects import failed: {e}")

    # Test modern app core interfaces
    try:
        print("\n✅ Testing core.interfaces.core_services import...")
        from core.interfaces.core_services import IUIStateManagementService
        print("   ✓ core.interfaces.core_services import successful")
    except ImportError as e:
        errors.append(f"core.interfaces.core_services: {e}")
        print(f"   ❌ core.interfaces.core_services import failed: {e}")

    try:
        print("\n✅ Testing core.interfaces.settings_interfaces import...")
        from core.interfaces.settings_interfaces import ISettingsService
        print("   ✓ core.interfaces.settings_interfaces import successful")
    except ImportError as e:
        errors.append(f"core.interfaces.settings_interfaces: {e}")
        print(f"   ❌ core.interfaces.settings_interfaces import failed: {e}")

    # Test application services
    try:
        print("\n✅ Testing application.services.settings.settings_service import...")
        from application.services.settings.settings_service import SettingsService
        print("   ✓ application.services.settings.settings_service import successful")
    except ImportError as e:
        errors.append(f"settings_service: {e}")
        print(f"   ❌ settings_service import failed: {e}")

    try:
        print("\n✅ Testing application.services.settings.user_profile_service import...")
        from application.services.settings.user_profile_service import UserProfileService
        print("   ✓ user_profile_service import successful")
    except ImportError as e:
        errors.append(f"user_profile_service: {e}")
        print(f"   ❌ user_profile_service import failed: {e}")

    # Test UI components
    try:
        print("\n✅ Testing presentation.components.ui.settings.coordinator import...")
        from presentation.components.ui.settings.coordinator import SettingsCoordinator
        print("   ✓ settings coordinator import successful")
    except ImportError as e:
        errors.append(f"settings_coordinator: {e}")
        print(f"   ❌ settings coordinator import failed: {e}")

    return errors

def main():
    """Main test function."""
    print("🧪 Running comprehensive import tests...")
    
    errors = test_imports()
    
    if not errors:
        print("\n🎉 All import tests passed! Your configuration is working correctly.")
        print("✅ PyQt6 is properly configured")
        print("✅ Launcher UI components are accessible")
        print("✅ Modern app services are accessible")
        print("✅ All Python paths are configured correctly")
        
        # Try to create some components
        try:
            print("\n🔧 Testing component instantiation...")
            from PyQt6.QtWidgets import QApplication
            
            app = QApplication.instance() or QApplication(sys.argv)
            
            # Test basic imports work by creating minimal instances
            from ui.reliable_effects import get_animation_manager
            animation_manager = get_animation_manager()
            print("   ✓ Animation manager created successfully")
            
            print("\n🎯 All tests completed successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Component instantiation failed: {e}")
            return False
    else:
        print(f"\n❌ {len(errors)} import errors found:")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
        
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure you're running this from the project root directory")
        print("2. Check that PyQt6 is installed: pip show PyQt6")
        print("3. Restart VSCode to reload configuration")
        print("4. Check that .pylintrc and .vscode/settings.json are properly configured")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
