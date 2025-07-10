#!/usr/bin/env python3
"""
Regression Test: Core Import Hook

Tests that the core import hook correctly resolves 'from core.*' imports
from various locations in the project.
"""

import sys
import os
import tempfile
from pathlib import Path
import importlib

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Install core import hook
import core_import_hook


def test_core_import_from_legacy_settings():
    """Test importing from legacy settings dialog location."""
    print("🧪 Testing core import from legacy settings dialog...")
    
    # Simulate being in the prop_button.py file location
    test_file_path = project_root / 'src' / 'desktop' / 'legacy' / 'src' / 'main_window' / 'main_widget' / 'settings_dialog' / 'ui' / 'prop_type' / 'test_import.py'
    
    # Create a temporary test file
    test_file_path.parent.mkdir(parents=True, exist_ok=True)
    test_content = '''
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parents[10]
sys.path.insert(0, str(project_root))

# Install core import hook
import core_import_hook

# Test the import
try:
    from core.glassmorphism_styler import GlassmorphismStyler
    print("✅ Successfully imported GlassmorphismStyler from core")
    print(f"✅ GlassmorphismStyler class: {GlassmorphismStyler}")
    
    # Test a method if it exists
    if hasattr(GlassmorphismStyler, 'get_color'):
        print("✅ GlassmorphismStyler.get_color method found")
    else:
        print("ℹ️ GlassmorphismStyler.get_color method not found (might be static)")
        
except ImportError as e:
    print(f"❌ Failed to import GlassmorphismStyler: {e}")
    sys.exit(1)
'''
    
    try:
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Run the test file
        import subprocess
        result = subprocess.run([sys.executable, str(test_file_path)], 
                              capture_output=True, text=True, cwd=str(project_root))
        
        print(f"📄 Test output:\n{result.stdout}")
        if result.stderr:
            print(f"⚠️ Test stderr:\n{result.stderr}")
        
        if result.returncode == 0:
            print("✅ Legacy settings dialog core import test PASSED")
        else:
            print("❌ Legacy settings dialog core import test FAILED")
        
        return result.returncode == 0
        
    finally:
        # Clean up test file
        if test_file_path.exists():
            test_file_path.unlink()


def test_direct_core_import():
    """Test direct core import from current context."""
    print("\n🧪 Testing direct core import...")
    
    try:
        # Test importing glassmorphism_styler
        from core.glassmorphism_styler import GlassmorphismStyler
        print("✅ Successfully imported GlassmorphismStyler directly")
        print(f"✅ GlassmorphismStyler: {GlassmorphismStyler}")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import GlassmorphismStyler directly: {e}")
        return False


def test_core_directory_discovery():
    """Test that we can find all available core directories."""
    print("\n🧪 Testing core directory discovery...")
    
    expected_core_dirs = [
        project_root / 'src' / 'desktop' / 'legacy' / 'src' / 'core',
        project_root / 'src' / 'desktop' / 'legacy' / 'src' / 'main_window' / 'main_widget' / 'settings_dialog' / 'core',
        project_root / 'src' / 'desktop' / 'modern' / 'src' / 'core',
        project_root / 'launcher' / 'core',
    ]
    
    found_cores = []
    for core_dir in expected_core_dirs:
        if core_dir.exists() and core_dir.is_dir():
            found_cores.append(core_dir)
            print(f"✅ Found core directory: {core_dir}")
            
            # List contents
            try:
                contents = list(core_dir.glob('*.py'))
                print(f"   📁 Contains {len(contents)} Python files: {[f.name for f in contents[:5]]}")
            except Exception as e:
                print(f"   ⚠️ Could not list contents: {e}")
    
    print(f"\n📊 Found {len(found_cores)} core directories out of {len(expected_core_dirs)} expected")
    return len(found_cores) > 0


def main():
    """Run all regression tests."""
    print("🏃‍♂️ Running Core Import Hook Regression Tests")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Core directory discovery
    if test_core_directory_discovery():
        tests_passed += 1
    
    # Test 2: Direct import
    if test_direct_core_import():
        tests_passed += 1
    
    # Test 3: Legacy settings dialog import
    if test_core_import_from_legacy_settings():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All regression tests PASSED!")
        return 0
    else:
        print("❌ Some regression tests FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
