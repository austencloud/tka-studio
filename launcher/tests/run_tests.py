#!/usr/bin/env python3
"""
Test runner for TKA Launcher tests.
"""

import sys
import subprocess
from pathlib import Path


def run_test_file(test_file: Path) -> bool:
    """Run a single test file and return success status."""
    print(f"\n🧪 Running {test_file.name}...")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            cwd=test_file.parent,
            capture_output=False,  # Show output directly
            text=True
        )
        
        success = result.returncode == 0
        print(f"\n{'✅ PASSED' if success else '❌ FAILED'}: {test_file.name}")
        return success
        
    except Exception as e:
        print(f"❌ ERROR running {test_file.name}: {e}")
        return False


def main():
    """Run all launcher tests."""
    print("🚀 TKA Launcher Test Suite")
    print("=" * 60)
    
    tests_dir = Path(__file__).parent
    
    # Find all test files
    test_files = [
        tests_dir / "test_horizontal_setup.py",
        tests_dir / "test_json_parsing.py",
    ]
    
    # Filter to only existing files
    existing_tests = [f for f in test_files if f.exists()]
    
    if not existing_tests:
        print("❌ No test files found!")
        return 1
    
    print(f"Found {len(existing_tests)} test files:")
    for test_file in existing_tests:
        print(f"  - {test_file.name}")
    
    # Run all tests
    results = []
    for test_file in existing_tests:
        success = run_test_file(test_file)
        results.append((test_file.name, success))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {status}: {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Launcher is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
