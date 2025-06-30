#!/usr/bin/env python3
"""
Quick verification script to check that all launcher test fixes are working.
Run this to verify all issues have been resolved.
"""

import sys
import subprocess
from pathlib import Path


def check_main_tests():
    """Check the main tests that were failing."""
    print("🔍 Checking main test fixes...")
    
    tests_to_check = [
        ("test_horizontal_setup.py", "Setup and configuration tests"),
        ("test_json_parsing.py", "JSON configuration parsing tests"),
    ]
    
    results = []
    tests_dir = Path(__file__).parent
    
    for test_file, description in tests_to_check:
        test_path = tests_dir / test_file
        print(f"\n📋 Running {test_file} - {description}")
        print("-" * 60)
        
        try:
            result = subprocess.run(
                [sys.executable, str(test_path)],
                cwd=tests_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            
            if success:
                print("✅ PASSED")
                # Show key success indicators
                if "All tests passed" in result.stdout:
                    print("   ✓ All internal tests passed")
                if "All imports successful" in result.stdout:
                    print("   ✓ All imports working")
                if "JSON parsed successfully" in result.stdout:
                    print("   ✓ JSON parsing working")
            else:
                print("❌ FAILED")
                print("STDOUT:", result.stdout[-300:])  # Last 300 chars
                print("STDERR:", result.stderr[-300:])  # Last 300 chars
            
            results.append((test_file, success))
            
        except subprocess.TimeoutExpired:
            print("⏰ TIMEOUT - Test took too long")
            results.append((test_file, False))
        except Exception as e:
            print(f"❌ ERROR - {e}")
            results.append((test_file, False))
    
    return results


def check_imports_directly():
    """Check imports directly to verify fixes."""
    print("\n🔍 Checking imports directly...")
    
    # Add launcher directory to path
    launcher_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(launcher_dir))
    
    import_tests = [
        ("config.settings", "SettingsManager"),
        ("integration.tka_integration", "TKAIntegrationService"),
        ("main", "TKAModernLauncherApp"),
    ]
    
    results = []
    
    for module_name, class_name in import_tests:
        try:
            print(f"📦 Importing {class_name} from {module_name}...")
            
            if module_name == "config.settings":
                from config.settings import SettingsManager
                # Test creating instance
                settings = SettingsManager()
                print(f"   ✓ SettingsManager created, mode: {settings.get('launch_mode')}")
                
            elif module_name == "integration.tka_integration":
                from integration.tka_integration import TKAIntegrationService
                # Test creating instance (but don't fully initialize to avoid side effects)
                print(f"   ✓ TKAIntegrationService import successful")
                
            elif module_name == "main":
                from main import TKAModernLauncherApp
                print(f"   ✓ TKAModernLauncherApp import successful")
            
            print(f"   ✅ {class_name} import PASSED")
            results.append((f"{module_name}.{class_name}", True))
            
        except Exception as e:
            print(f"   ❌ {class_name} import FAILED: {e}")
            results.append((f"{module_name}.{class_name}", False))
    
    return results


def main():
    """Main verification function."""
    print("🚀 TKA Launcher Test Fixes Verification")
    print("=" * 60)
    print("This script verifies that all the test fixes are working correctly.")
    print()
    
    # Check direct imports first
    import_results = check_imports_directly()
    
    # Check main tests
    test_results = check_main_tests()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    print("\n🔧 Import Tests:")
    for test_name, success in import_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print("\n🧪 Test Files:")
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    # Overall result
    all_results = import_results + test_results
    total_passed = sum(1 for _, success in all_results if success)
    total_tests = len(all_results)
    
    print(f"\n📈 Overall: {total_passed}/{total_tests} checks passed")
    
    if total_passed == total_tests:
        print("\n🎉 All fixes verified! All tests should now work correctly.")
        print("\n💡 You can now run:")
        print("   python launcher/tests/run_tests.py")
        print("   python launcher/tests/test_horizontal_setup.py")
        print("   python launcher/tests/test_json_parsing.py")
        return 0
    else:
        print("\n⚠️ Some issues remain. Check the failed tests above.")
        print("\n🔧 Common fixes:")
        print("   - Ensure you're in the right directory")
        print("   - Check Python path and imports")
        print("   - Verify required files exist")
        return 1


if __name__ == "__main__":
    sys.exit(main())
