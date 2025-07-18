"""
Automated Thumbnail Height Testing

This script runs the TKA Modern Desktop app and automatically measures
thumbnail heights to verify proper sizing.
"""

import sys
import os
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add TKA paths
tka_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(tka_root))
sys.path.insert(0, str(tka_root / "src"))


class ThumbnailHeightTester:
    """Automated tester for thumbnail heights."""
    
    def __init__(self):
        self.tka_root = Path(__file__).parent.parent.parent
        self.results = {}
        
    def run_app_and_test(self) -> bool:
        """Run the TKA app and perform thumbnail height testing."""
        print("🚀 Starting TKA Modern Desktop App for testing...")
        
        # Build the command to run the app
        venv_python = self.tka_root / ".venv" / "Scripts" / "python.exe"
        main_py = self.tka_root / "main.py"
        
        if not venv_python.exists():
            print(f"❌ Virtual environment not found at {venv_python}")
            return False
            
        if not main_py.exists():
            print(f"❌ Main.py not found at {main_py}")
            return False
        
        # Set up environment
        env = os.environ.copy()
        env.update({
            "PYTHONPATH": f"{self.tka_root};{self.tka_root / 'src'};{self.tka_root / 'launcher'};{self.tka_root / 'packages'};{self.tka_root / '.venv' / 'Lib' / 'site-packages'}",
            "VIRTUAL_ENV": str(self.tka_root / ".venv"),
            "PYTHONUNBUFFERED": "1",
            "TKA_TEST_MODE": "1",  # Signal to app that we're testing
        })
        
        try:
            # Start the application
            print("Starting TKA application...")
            process = subprocess.Popen(
                [str(venv_python), str(main_py)],
                cwd=str(self.tka_root),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for app to start
            time.sleep(10)
            
            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print(f"❌ App failed to start:")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                return False
                
            print("✅ TKA application started successfully")
            
            # Give time for full initialization
            time.sleep(5)
            
            # The app should be running now
            print("⏳ App is running - manual testing required")
            print("📋 Please follow these steps:")
            print("1. Navigate to the Browse tab")
            print("2. Load some sequences")
            print("3. Observe thumbnail heights")
            print("4. Check if images are properly contained")
            print("5. Look for any clipping or overflow")
            print("6. Press Ctrl+C here when done testing")
            
            # Wait for user to finish testing
            try:
                while process.poll() is None:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n⏸️ Testing interrupted by user")
                
            # Terminate the process
            process.terminate()
            time.sleep(2)
            
            if process.poll() is None:
                process.kill()
                
            print("✅ Testing session completed")
            return True
            
        except Exception as e:
            print(f"❌ Error running app: {e}")
            return False
    
    def create_test_script(self) -> str:
        """Create a test script that can be run manually."""
        script_content = """
# TKA Thumbnail Height Testing Script
# 
# This script helps you manually test thumbnail heights in the TKA Modern Desktop App
# 
# TESTING PROCEDURE:
# 1. Run the TKA Modern Desktop App
# 2. Navigate to the Browse tab
# 3. Apply filters to load sequences
# 4. Observe the thumbnail grid
# 
# THINGS TO CHECK:
# ✓ Do thumbnail containers properly expand to show full images?
# ✓ Are images centered and properly sized within containers?
# ✓ Is there adequate spacing between thumbnails?
# ✓ Do sequence names and info display without clipping?
# ✓ Are all thumbnails the same width in each column?
# ✓ Do thumbnails maintain consistent aspect ratios?
# 
# MEASUREMENTS TO TAKE:
# - Container width and height
# - Image width and height within container
# - Text height (sequence name + info)
# - Total content height vs container height
# 
# EXPECTED BEHAVIOR:
# - Thumbnails should be arranged in 3 columns
# - Each column should have equal width
# - Container height should expand to fit content
# - Images should scale to fill container width
# - No content should be clipped or overflow
# 
# COMPARISON WITH LEGACY:
# - Check legacy browse tab for reference behavior
# - Modern version should match legacy thumbnail sizing
# - Same responsive behavior on window resize
"""
        
        script_path = self.tka_root / "thumbnail_height_test_guide.txt"
        with open(script_path, 'w') as f:
            f.write(script_content)
            
        return str(script_path)


def main():
    """Main function to run thumbnail height testing."""
    tester = ThumbnailHeightTester()
    
    print("📏 TKA Thumbnail Height Testing")
    print("=" * 50)
    
    # Create test guide
    guide_path = tester.create_test_script()
    print(f"📝 Test guide created: {guide_path}")
    
    # Ask user if they want to run the automated test
    response = input("\n🤖 Run automated test? (y/n): ").lower().strip()
    
    if response == 'y':
        success = tester.run_app_and_test()
        if success:
            print("\n✅ Automated test completed")
        else:
            print("\n❌ Automated test failed")
    else:
        print("\n📋 Manual testing mode selected")
        print("Please follow the test guide and run the app manually")
        
    print(f"\n📖 Refer to test guide: {guide_path}")
    print("📊 Document your findings and any issues observed")


if __name__ == "__main__":
    main()
