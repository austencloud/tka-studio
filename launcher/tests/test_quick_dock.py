#!/usr/bin/env python3
"""
Quick test to verify launcher starts in dock mode.
"""

import sys
import tempfile
import os
import logging
from pathlib import Path

# Add launcher directory to path
sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_current_dock_mode():
    """Test the current dock mode configuration."""
    try:
        from config.settings import SettingsManager
        
        # Use the real settings (not a temp directory)
        settings_manager = SettingsManager()
        
        launch_mode = settings_manager.get("launch_mode")
        auto_start_docked = settings_manager.get("auto_start_docked")
        should_dock = settings_manager.should_restore_to_docked()
        
        print(f"Current launch_mode: {launch_mode}")
        print(f"Current auto_start_docked: {auto_start_docked}")
        print(f"Should restore to docked: {should_dock}")
        
        if launch_mode == "docked" and should_dock:
            print("✅ Settings are correctly configured for dock mode!")
            return True
        else:
            print("❌ Settings are NOT configured for dock mode")
            return False
            
    except Exception as e:
        print(f"❌ Error checking settings: {e}")
        return False

if __name__ == "__main__":
    test_current_dock_mode()
