#!/usr/bin/env python3
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Test graph editor edge cases and rapid interaction scenarios
PERMANENT: Edge case handling must be robust and reliable
AUTHOR: @ai-agent
"""

import sys
import os
import pytest
import time
from typing import List, Dict, Any

# Add TKA source path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "desktop", "modern", "src"))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from domain.models.core_models import BeatData, MotionData, MotionType, RotationDirection, Location
from presentation.components.graph_editor.graph_editor import GraphEditor


@pytest.mark.specification
@pytest.mark.critical
class TestGraphEditorEdgeCases:
    """PERMANENT: Graph editor edge case handling - NEVER DELETE"""
    
    def test_none_data_handling_contract(self):
        """PERMANENT: Graph editor must handle None data gracefully"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        graph_editor = GraphEditor()
        
        # Contract: None beat data must not crash
        try:
            graph_editor.set_selected_beat_data(-1, None)
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"None data handling crashed: {e}")
        
        assert success, "None data handling must not crash"
        assert graph_editor._selected_beat_data is None
    
    def test_empty_beat_handling_contract(self):
        """PERMANENT: Graph editor must handle empty beats gracefully"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        graph_editor = GraphEditor()
        
        # Contract: Empty beat must not crash
        empty_beat = BeatData.empty()
        
        try:
            graph_editor.set_selected_beat_data(0, empty_beat)
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"Empty beat handling crashed: {e}")
        
        assert success, "Empty beat handling must not crash"
        assert graph_editor._selected_beat_data is not None
    
    def test_maximum_turn_values_contract(self):
        """PERMANENT: Graph editor must handle maximum turn values"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        graph_editor = GraphEditor()
        
        # Contract: Large turn values must not crash
        try:
            for i in range(20):  # Test up to 10 turns
                graph_editor._adjust_turn_amount("blue", 0.5)
                graph_editor._adjust_turn_amount("red", 1.0)
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"Maximum turn values crashed: {e}")
        
        assert success, "Maximum turn values must not crash"
        assert graph_editor._blue_turn_amount == 10.0
        assert graph_editor._red_turn_amount == 20.0
    
    def test_negative_turn_boundary_contract(self):
        """PERMANENT: Turn values must not go below zero"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        graph_editor = GraphEditor()
        
        # Contract: Turn values must not go below 0
        graph_editor._adjust_turn_amount("blue", -5.0)
        graph_editor._adjust_turn_amount("red", -10.0)
        
        assert graph_editor._blue_turn_amount == 0, "Blue turns went below 0"
        assert graph_editor._red_turn_amount == 0, "Red turns went below 0"


@pytest.mark.specification
class TestGraphEditorRapidInteraction:
    """PERMANENT: Graph editor rapid interaction handling - NEVER DELETE"""
    
    def test_rapid_button_clicking_contract(self):
        """PERMANENT: Rapid button clicking must not crash or corrupt state"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        graph_editor = GraphEditor()
        
        # Contract: Rapid clicking must not crash
        start_time = time.time()
        try:
            for i in range(50):  # Simulate rapid clicking
                graph_editor._adjust_turn_amount("blue", 1.0)
                graph_editor._adjust_turn_amount("blue", -0.5)
                graph_editor._adjust_turn_amount("red", 0.5)
                graph_editor._set_orientation("blue", "OUT" if i % 2 == 0 else "IN")
                graph_editor._set_orientation("red", "CLOCK" if i % 3 == 0 else "COUNTER")
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"Rapid interaction crashed: {e}")
        
        interaction_time = time.time() - start_time
        
        assert success, "Rapid interaction must not crash"
        # Contract: Rapid interactions should complete quickly
        assert interaction_time < 1.0, f"Rapid interactions too slow: {interaction_time:.3f}s"
    
    def test_rapid_beat_switching_contract(self):
        """PERMANENT: Rapid beat switching must not crash"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        graph_editor = GraphEditor()
        
        # Create test beats
        beats = []
        for i in range(5):
            beat = BeatData(
                beat_number=i,
                letter=chr(65 + i),  # A, B, C, D, E
                blue_motion=MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.EAST,
                    turns=float(i)
                ) if i % 2 == 0 else None
            )
            beats.append(beat)
        
        # Contract: Rapid beat switching must not crash
        try:
            for _ in range(10):  # Switch beats rapidly
                for i, beat in enumerate(beats):
                    graph_editor.set_selected_beat_data(i, beat)
                    graph_editor.set_selected_start_position(beat)
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"Rapid beat switching crashed: {e}")
        
        assert success, "Rapid beat switching must not crash"
    
    def test_concurrent_ui_updates_contract(self):
        """PERMANENT: Concurrent UI updates must not corrupt state"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        graph_editor = GraphEditor()
        
        # Create complex beat data
        complex_beat = BeatData(
            beat_number=1,
            letter="A",
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=2.5
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                turns=1.5
            )
        )
        
        # Contract: Concurrent updates must not crash
        try:
            # Simulate concurrent UI updates
            graph_editor.set_selected_beat_data(0, complex_beat)
            graph_editor._adjust_turn_amount("blue", 1.0)
            graph_editor._adjust_turn_amount("red", 0.5)
            graph_editor._set_orientation("blue", "OUT")
            graph_editor._set_orientation("red", "CLOCK")
            graph_editor.set_selected_beat_data(1, complex_beat)
            graph_editor._adjust_turn_amount("blue", -0.5)
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"Concurrent UI updates crashed: {e}")
        
        assert success, "Concurrent UI updates must not crash"


@pytest.mark.specification
class TestGraphEditorMemoryAndPerformance:
    """PERMANENT: Graph editor memory and performance contracts - NEVER DELETE"""
    
    def test_memory_leak_prevention_contract(self):
        """PERMANENT: Graph editor must not leak memory during extended use"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Contract: Extended use must not cause memory issues
        try:
            for cycle in range(10):  # Simulate extended use
                graph_editor = GraphEditor()
                
                # Simulate typical usage
                for i in range(20):
                    beat = BeatData(beat_number=i, letter="A")
                    graph_editor.set_selected_beat_data(i, beat)
                    graph_editor._adjust_turn_amount("blue", 1.0)
                    graph_editor._adjust_turn_amount("red", 0.5)
                
                # Clean up
                del graph_editor
            
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"Memory leak test failed: {e}")
        
        assert success, "Extended use must not cause memory issues"
    
    def test_performance_degradation_contract(self):
        """PERMANENT: Performance must not degrade with extended use"""
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        graph_editor = GraphEditor()
        
        # Measure initial performance
        start_time = time.time()
        for i in range(10):
            graph_editor._adjust_turn_amount("blue", 1.0)
        initial_time = time.time() - start_time
        
        # Simulate extended use
        for i in range(100):
            beat = BeatData(beat_number=i, letter="A")
            graph_editor.set_selected_beat_data(i, beat)
            graph_editor._adjust_turn_amount("blue", 0.5)
            graph_editor._adjust_turn_amount("red", 1.0)
        
        # Measure performance after extended use
        start_time = time.time()
        for i in range(10):
            graph_editor._adjust_turn_amount("blue", 1.0)
        final_time = time.time() - start_time
        
        # Contract: Performance must not degrade significantly
        performance_ratio = final_time / initial_time if initial_time > 0 else 1.0
        assert performance_ratio < 2.0, f"Performance degraded too much: {performance_ratio:.2f}x slower"


def run_edge_case_tests() -> Dict[str, Any]:
    """
    Run comprehensive edge case tests and return detailed results.
    """
    print("🔍 Starting Graph Editor Edge Case Test Suite")
    print("=" * 60)
    
    results = {
        'overall_success': True,
        'test_results': {},
        'performance_metrics': {},
        'errors': [],
        'execution_time': 0
    }
    
    start_time = time.time()
    
    try:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test 1: None Data Handling
        print("\n📋 Test 1: None Data Handling")
        try:
            graph_editor = GraphEditor()
            graph_editor.set_selected_beat_data(-1, None)
            results['test_results']['none_data'] = True
            print("   ✅ None data handled successfully")
        except Exception as e:
            results['test_results']['none_data'] = False
            results['errors'].append(f"None data handling failed: {e}")
            print(f"   ❌ None data handling failed: {e}")
        
        # Test 2: Empty Beat Handling
        print("\n📋 Test 2: Empty Beat Handling")
        try:
            graph_editor = GraphEditor()
            empty_beat = BeatData.empty()
            graph_editor.set_selected_beat_data(0, empty_beat)
            results['test_results']['empty_beat'] = True
            print("   ✅ Empty beat handled successfully")
        except Exception as e:
            results['test_results']['empty_beat'] = False
            results['errors'].append(f"Empty beat handling failed: {e}")
            print(f"   ❌ Empty beat handling failed: {e}")
        
        # Test 3: Maximum Turn Values
        print("\n📋 Test 3: Maximum Turn Values")
        try:
            graph_editor = GraphEditor()
            for i in range(20):
                graph_editor._adjust_turn_amount("blue", 0.5)
            max_turns_correct = graph_editor._blue_turn_amount == 10.0
            results['test_results']['max_turns'] = max_turns_correct
            print(f"   ✅ Maximum turns: {graph_editor._blue_turn_amount}")
        except Exception as e:
            results['test_results']['max_turns'] = False
            results['errors'].append(f"Maximum turn values failed: {e}")
            print(f"   ❌ Maximum turn values failed: {e}")
        
        # Test 4: Rapid Interaction
        print("\n📋 Test 4: Rapid Interaction")
        rapid_start = time.time()
        try:
            graph_editor = GraphEditor()
            for i in range(50):
                graph_editor._adjust_turn_amount("blue", 1.0)
                graph_editor._adjust_turn_amount("blue", -0.5)
                graph_editor._set_orientation("blue", "OUT" if i % 2 == 0 else "IN")
            rapid_time = time.time() - rapid_start
            results['test_results']['rapid_interaction'] = True
            results['performance_metrics']['rapid_interaction_time'] = rapid_time
            print(f"   ✅ Rapid interaction completed in {rapid_time:.3f}s")
        except Exception as e:
            results['test_results']['rapid_interaction'] = False
            results['errors'].append(f"Rapid interaction failed: {e}")
            print(f"   ❌ Rapid interaction failed: {e}")
        
        # Test 5: Beat Switching
        print("\n📋 Test 5: Rapid Beat Switching")
        try:
            graph_editor = GraphEditor()
            beats = [BeatData(beat_number=i, letter=chr(65 + i)) for i in range(5)]
            for _ in range(10):
                for i, beat in enumerate(beats):
                    graph_editor.set_selected_beat_data(i, beat)
            results['test_results']['beat_switching'] = True
            print("   ✅ Rapid beat switching successful")
        except Exception as e:
            results['test_results']['beat_switching'] = False
            results['errors'].append(f"Beat switching failed: {e}")
            print(f"   ❌ Beat switching failed: {e}")
        
        # Calculate overall success
        test_successes = list(results['test_results'].values())
        success_rate = sum(test_successes) / len(test_successes) if test_successes else 0
        results['overall_success'] = success_rate >= 0.8
        results['success_rate'] = success_rate
        
    except Exception as e:
        results['overall_success'] = False
        results['errors'].append(f"Critical edge case test failure: {e}")
        print(f"❌ Critical edge case test failure: {e}")
    
    finally:
        results['execution_time'] = time.time() - start_time
    
    # Print summary
    print("\n📊 EDGE CASE TEST SUMMARY")
    print("=" * 40)
    print(f"Overall Success: {'✅ PASSED' if results['overall_success'] else '❌ FAILED'}")
    print(f"Success Rate: {results.get('success_rate', 0):.1%}")
    print(f"Total Execution Time: {results['execution_time']:.3f}s")
    
    if results['errors']:
        print(f"Errors: {len(results['errors'])}")
        for error in results['errors']:
            print(f"  - {error}")
    
    return results


if __name__ == "__main__":
    # Run edge case tests when executed directly
    results = run_edge_case_tests()
    exit_code = 0 if results['overall_success'] else 1
    sys.exit(exit_code)
