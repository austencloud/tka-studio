#!/usr/bin/env python3
"""
Test script to verify GUI application launching works correctly.
"""

import subprocess
import sys
from pathlib import Path

def test_gui_launch():
    """Test launching TKA Desktop with proper GUI subprocess configuration."""
    
    # Get the TKA root directory (parent of launcher directory)
    tka_root = Path(__file__).parent.parent
    command = "python main.py --modern"
    
    print(f"Testing GUI application launch:")
    print(f"  Command: {command}")
    print(f"  Working directory: {tka_root}")
    print(f"  Absolute path: {tka_root.absolute()}")
    
    try:
        # Launch with GUI-friendly subprocess configuration
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=str(tka_root),
            # Allow GUI applications to display by not capturing output
            stdout=None,
            stderr=None,
            # Detach from parent process so GUI apps can run independently
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP') else 0,
        )
        
        print(f"✅ Process launched successfully with PID: {process.pid}")
        print("🪟 Check if TKA Desktop window appeared on your screen!")
        print("   The application should be visible and interactive.")
        
        return True
        
    except Exception as e:
        print(f"❌ Launch failed: {e}")
        return False

if __name__ == "__main__":
    test_gui_launch()
