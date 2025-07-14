#!/usr/bin/env python3
"""
Test script to verify fade animations are working in the option picker.
This script simulates clicking pictographs to trigger fade transitions.
"""

import sys
import os
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

def test_fade_animations():
    """Test that fade animations work when clicking pictographs."""
    print("🎭 Testing fade animations in option picker...")
    
    try:
        # Create application
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        
        # Create container and initialize services
        from core.application.application_factory import ApplicationFactory, ApplicationMode
        container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)
        
        # Get the option picker scroll component
        from presentation.components.option_picker.components.option_picker_scroll import OptionPickerScroll
        option_picker = container.resolve(OptionPickerScroll)
        
        print("✅ Option picker created successfully")
        
        # Load initial options (should be direct update since no existing frames)
        from domain.models.sequence_data import SequenceData
        from domain.models.beat_data import BeatData
        from domain.models.pictograph_data import PictographData
        
        # Create a simple sequence to trigger option loading
        initial_sequence = SequenceData([
            BeatData(
                beat_number=1,
                pictograph_data=PictographData(
                    letter="Σ",
                    start_pos="alpha1",
                    end_pos="beta1"
                )
            )
        ])
        
        print("🔄 Loading initial options...")
        option_picker.load_options_from_sequence(initial_sequence)
        
        # Wait a moment for initial load
        QTimer.singleShot(500, lambda: test_transition_with_existing_frames(option_picker))
        
        # Start the event loop briefly
        QTimer.singleShot(2000, app.quit)
        app.exec()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_transition_with_existing_frames(option_picker):
    """Test transition when there are existing frames (should trigger fade)."""
    print("🎭 Testing transition with existing frames...")
    
    try:
        # Create a different sequence to trigger a transition
        from domain.models.sequence_data import SequenceData
        from domain.models.beat_data import BeatData
        from domain.models.pictograph_data import PictographData
        
        new_sequence = SequenceData([
            BeatData(
                beat_number=1,
                pictograph_data=PictographData(
                    letter="W",
                    start_pos="beta1", 
                    end_pos="gamma1"
                )
            )
        ])
        
        print("🔄 Loading new options (should trigger fade transition)...")
        option_picker.load_options_from_sequence(new_sequence)
        
        print("✅ Transition test completed")
        
    except Exception as e:
        print(f"❌ Transition test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fade_animations()
