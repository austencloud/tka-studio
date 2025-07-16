#!/usr/bin/env python3
"""
Simple delete beat test that can be run from within the application.
"""

import sys
import os
from typing import Optional

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest

from domain.models.beat_data import BeatData
from domain.models.sequence_data import SequenceData


def test_delete_beat_functionality():
    """Test delete beat functionality with real UI components."""
    print("🧪 [DELETE_BEAT_TEST] Starting delete beat functionality test...")
    
    try:
        # Get the running application
        app = QApplication.instance()
        if not app:
            print("❌ [DELETE_BEAT_TEST] No QApplication instance found")
            return False
        
        # Find the main window and components
        main_window = None
        for widget in app.topLevelWidgets():
            if hasattr(widget, 'construct_tab'):
                main_window = widget
                break
        
        if not main_window:
            print("❌ [DELETE_BEAT_TEST] Could not find main window")
            return False
        
        construct_tab = main_window.construct_tab
        workbench = construct_tab.workbench if hasattr(construct_tab, 'workbench') else None
        
        if not workbench:
            print("❌ [DELETE_BEAT_TEST] Could not find workbench")
            return False
        
        print("✅ [DELETE_BEAT_TEST] Found main components")
        
        # Step 1: Create a test sequence with multiple beats
        print("📝 [DELETE_BEAT_TEST] Creating test sequence...")
        
        beats = [
            BeatData(beat_number=1, metadata={"letter": "J"}),
            BeatData(beat_number=2, metadata={"letter": "θ"}),
            BeatData(beat_number=3, metadata={"letter": "X"}),
            BeatData(beat_number=4, metadata={"letter": "Σ"}),
            BeatData(beat_number=5, metadata={"letter": "W"}),
        ]
        
        test_sequence = SequenceData(
            id="delete_beat_test",
            beats=beats,
            start_position="beta3"
        )
        
        # Set the sequence in the workbench
        workbench.set_sequence(test_sequence)
        QTest.qWait(1000)  # Wait for UI to update
        
        # Verify sequence was set
        current_sequence = workbench._state_manager.get_current_sequence()
        if not current_sequence or len(current_sequence.beats) != 5:
            print(f"❌ [DELETE_BEAT_TEST] Failed to set test sequence. Got {len(current_sequence.beats) if current_sequence else 0} beats")
            return False
        
        print(f"✅ [DELETE_BEAT_TEST] Test sequence created with {len(current_sequence.beats)} beats")
        print(f"📊 [DELETE_BEAT_TEST] Sequence: {[beat.letter for beat in current_sequence.beats]}")
        
        # Step 2: Test beat selection
        print("🎯 [DELETE_BEAT_TEST] Testing beat selection...")
        
        beat_frame = workbench._beat_frame_section
        if not beat_frame:
            print("❌ [DELETE_BEAT_TEST] Could not find beat frame")
            return False
        
        # Try to select beat at index 2 (X)
        try:
            if hasattr(beat_frame, 'select_beat'):
                beat_frame.select_beat(2)
                QTest.qWait(500)
                
                selected_index = beat_frame.get_selected_beat_index()
                print(f"📊 [DELETE_BEAT_TEST] Selected beat index: {selected_index}")
                
                if selected_index != 2:
                    print(f"❌ [DELETE_BEAT_TEST] Beat selection failed. Expected 2, got {selected_index}")
                    return False
                
                print("✅ [DELETE_BEAT_TEST] Beat selection successful")
            else:
                print("❌ [DELETE_BEAT_TEST] Beat frame has no select_beat method")
                return False
        except Exception as e:
            print(f"❌ [DELETE_BEAT_TEST] Beat selection failed: {e}")
            return False
        
        # Step 3: Test delete beat operation
        print("🗑️ [DELETE_BEAT_TEST] Testing delete beat operation...")
        
        try:
            # Get the operation coordinator
            operation_coordinator = workbench._operation_coordinator
            if not operation_coordinator:
                print("❌ [DELETE_BEAT_TEST] Could not find operation coordinator")
                return False
            
            # Execute delete beat operation
            result = operation_coordinator.delete_beat(2)  # Delete beat at index 2
            
            if not result.success:
                print(f"❌ [DELETE_BEAT_TEST] Delete beat operation failed: {result.message}")
                return False
            
            print(f"✅ [DELETE_BEAT_TEST] Delete beat operation successful: {result.message}")
            
            # Wait for UI to update
            QTest.qWait(1000)
            
            # Verify the result
            updated_sequence = workbench._state_manager.get_current_sequence()
            if not updated_sequence:
                print("❌ [DELETE_BEAT_TEST] No sequence after delete operation")
                return False
            
            remaining_beats = [beat.letter for beat in updated_sequence.beats]
            print(f"📊 [DELETE_BEAT_TEST] Remaining beats: {remaining_beats}")
            
            # Should have 2 beats remaining (J, θ) since we deleted X and all following
            expected_beats = ["J", "θ"]
            if remaining_beats == expected_beats:
                print("✅ [DELETE_BEAT_TEST] Delete beat and following logic working correctly!")
                return True
            else:
                print(f"❌ [DELETE_BEAT_TEST] Unexpected result. Expected {expected_beats}, got {remaining_beats}")
                return False
                
        except Exception as e:
            print(f"❌ [DELETE_BEAT_TEST] Delete beat operation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ [DELETE_BEAT_TEST] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_start_position_deletion():
    """Test start position deletion (delete all beats)."""
    print("🧪 [DELETE_BEAT_TEST] Testing start position deletion...")
    
    try:
        # Get the running application
        app = QApplication.instance()
        if not app:
            print("❌ [DELETE_BEAT_TEST] No QApplication instance found")
            return False
        
        # Find components (same as above)
        main_window = None
        for widget in app.topLevelWidgets():
            if hasattr(widget, 'construct_tab'):
                main_window = widget
                break
        
        if not main_window:
            print("❌ [DELETE_BEAT_TEST] Could not find main window")
            return False
        
        workbench = main_window.construct_tab.workbench
        if not workbench:
            print("❌ [DELETE_BEAT_TEST] Could not find workbench")
            return False
        
        # Create test sequence
        beats = [
            BeatData(beat_number=1, metadata={"letter": "J"}),
            BeatData(beat_number=2, metadata={"letter": "θ"}),
        ]
        
        test_sequence = SequenceData(
            id="start_pos_delete_test",
            beats=beats,
            start_position="beta3"
        )
        
        workbench.set_sequence(test_sequence)
        QTest.qWait(1000)
        
        print(f"📊 [DELETE_BEAT_TEST] Initial sequence: {[beat.letter for beat in test_sequence.beats]}")
        
        # Test start position deletion (beat_index = -1)
        operation_coordinator = workbench._operation_coordinator
        result = operation_coordinator.delete_beat(-1)  # Start position deletion
        
        if not result.success:
            print(f"❌ [DELETE_BEAT_TEST] Start position deletion failed: {result.message}")
            return False
        
        QTest.qWait(1000)
        
        # Verify all beats were deleted
        updated_sequence = workbench._state_manager.get_current_sequence()
        if updated_sequence and len(updated_sequence.beats) == 0:
            print("✅ [DELETE_BEAT_TEST] Start position deletion successful - all beats removed!")
            return True
        else:
            remaining_count = len(updated_sequence.beats) if updated_sequence else "unknown"
            print(f"❌ [DELETE_BEAT_TEST] Start position deletion failed. {remaining_count} beats remaining")
            return False
            
    except Exception as e:
        print(f"❌ [DELETE_BEAT_TEST] Start position deletion test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_delete_beat_tests():
    """Run all delete beat tests."""
    print("🚀 [DELETE_BEAT_TEST] Running all delete beat tests...")
    
    tests = [
        ("Delete Beat and Following", test_delete_beat_functionality),
        ("Start Position Deletion", test_start_position_deletion),
    ]
    
    results = {}
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n🧪 [DELETE_BEAT_TEST] Running: {test_name}")
        try:
            result = test_func()
            results[test_name] = result
            if result:
                print(f"✅ [DELETE_BEAT_TEST] {test_name} PASSED")
            else:
                print(f"❌ [DELETE_BEAT_TEST] {test_name} FAILED")
                all_passed = False
        except Exception as e:
            print(f"❌ [DELETE_BEAT_TEST] {test_name} ERROR: {e}")
            results[test_name] = False
            all_passed = False
    
    # Print summary
    print(f"\n📊 [DELETE_BEAT_TEST] Test Summary:")
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    if all_passed:
        print("\n🎉 All delete beat tests PASSED!")
    else:
        print("\n❌ Some delete beat tests FAILED!")
    
    return all_passed


if __name__ == "__main__":
    run_all_delete_beat_tests()
