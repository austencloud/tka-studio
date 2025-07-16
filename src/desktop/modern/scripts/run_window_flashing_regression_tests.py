#!/usr/bin/env python3
"""
Run regression tests to ensure window flashing issue doesn't return.
"""

import sys
import subprocess
import os

def run_regression_tests():
    """Run the window flashing regression tests."""
    print("=" * 80)
    print("🧪 RUNNING WINDOW FLASHING REGRESSION TESTS")
    print("=" * 80)
    
    # Change to the correct directory
    os.chdir('src/desktop/modern')
    
    # Add src to Python path
    sys.path.insert(0, 'src')
    
    try:
        # Run the specific regression test
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/regression/test_advanced_picker_no_window_flashing.py',
            '-v',  # Verbose output
            '--tb=short'  # Short traceback format
        ], capture_output=True, text=True, cwd='.')
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n" + "=" * 80)
            print("✅ ALL REGRESSION TESTS PASSED!")
            print("✅ Window flashing issue is confirmed fixed!")
            print("=" * 80)
            return True
        else:
            print("\n" + "=" * 80)
            print("❌ REGRESSION TESTS FAILED!")
            print("❌ Window flashing issue may have returned!")
            print("=" * 80)
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_regression_tests()
    sys.exit(0 if success else 1)
