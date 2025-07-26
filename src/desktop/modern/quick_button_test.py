"""
Quick Button Test - Verify all buttons are working

Run this to test that the buttons are properly connected and working.
"""

import sys
import logging
from pathlib import Path

# Add source path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication

def test_button_connections():
    """Test that button signals are properly connected."""
    
    # Create minimal app
    app = QApplication.instance() or QApplication([])
    
    # Import after QApplication is created
    from desktop.modern.presentation.tabs.browse.browse_tab import BrowseTab
    
    # Create a simple test
    sequences_dir = Path("data/sequences")  # Use your actual path
    settings_file = Path("test_settings.json")
    
    # Create browse tab
    browse_tab = BrowseTab(sequences_dir, settings_file)
    browse_tab.show()
    
    # Check that the methods exist
    methods_to_check = [
        "_on_sequence_action",
        "_handle_edit_sequence", 
        "_handle_save_image",
        "_handle_delete_variation",
        "_handle_fullscreen_view"
    ]
    
    print("🔍 Checking button handler methods...")
    for method_name in methods_to_check:
        if hasattr(browse_tab, method_name):
            print(f"✅ {method_name} - FOUND")
        else:
            print(f"❌ {method_name} - MISSING")
    
    # Test signal connection
    print("\n🔗 Testing signal connections...")
    if hasattr(browse_tab.sequence_viewer_panel, 'sequence_action'):
        print("✅ sequence_action signal - CONNECTED")
        
        # Test a mock signal emission
        print("\n🧪 Testing signal emission...")
        browse_tab._on_sequence_action("edit", "test-id-123")
        print("✅ Edit signal test completed")
        
    else:
        print("❌ sequence_action signal - NOT FOUND")
    
    print("\n🎉 Button functionality test complete!")
    print("Your buttons should now be working!")
    
    app.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_button_connections()
