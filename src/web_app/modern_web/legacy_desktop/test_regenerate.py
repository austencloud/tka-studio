#!/usr/bin/env python3
"""
Test script to verify the regenerate functionality works correctly.
"""

import sys
import os

# Add the legacy path to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_window.main_widget.sequence_card_tab.export.image_exporter import SequenceCardImageExporter

def test_force_regenerate_flag():
    """Test that the force_regenerate flag works correctly."""
    
    # Create an instance of the image exporter
    exporter = SequenceCardImageExporter(None)  # Pass None for parent since we're just testing
    
    # Test default state
    assert not getattr(exporter, 'force_regenerate', False), "force_regenerate should default to False"
    
    # Test setting the flag
    exporter.force_regenerate = True
    assert exporter.force_regenerate, "force_regenerate should be True when set"
    
    # Test the _needs_regeneration method with force_regenerate = True
    needs_regen, reason = exporter._needs_regeneration("dummy_source.json", "dummy_output.png")
    assert needs_regen, "Should need regeneration when force_regenerate is True"
    assert reason == "Force regeneration requested", f"Expected 'Force regeneration requested', got '{reason}'"
    
    # Test with force_regenerate = False
    exporter.force_regenerate = False
    # This will return True because the files don't exist, but the reason should be different
    needs_regen, reason = exporter._needs_regeneration("dummy_source.json", "dummy_output.png")
    assert needs_regen, "Should need regeneration when output doesn't exist"
    assert reason == "Output file does not exist", f"Expected 'Output file does not exist', got '{reason}'"
    
    print("✅ All tests passed! The force_regenerate functionality is working correctly.")

if __name__ == "__main__":
    test_force_regenerate_flag()
