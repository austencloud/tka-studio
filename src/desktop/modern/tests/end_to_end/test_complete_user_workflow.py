#!/usr/bin/env python3
"""
COMPLETE USER WORKFLOW TEST: The exact sequence user described
MANDATORY: Test the exact workflow that reveals the picker transition bug

This test validates:
1. Start up the program
2. Select start position in start position picker
3. Select option in option picker
4. Click Clear Sequence button
5. Verify it correctly resets to start position picker
"""

import sys
import time
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtCore import QTimer
from PyQt6.QtTest import QTest

from core.application.application_factory import ApplicationFactory
from application.services.core.sequence_persistence_service import SequencePersistenceService


class CompleteUserWorkflowTester:
    """Test the complete user workflow that reveals the bug"""
    
    def __init__(self):
        self.app = None
        self.container = None
        self.persistence_service = None
        self.construct_tab = None
        self.layout_manager = None
        self.workbench = None
        self.workflow_log = []
        
    def setup_fresh_environment(self) -> bool:
        """Setup a completely fresh environment"""
        print("🚀 [WORKFLOW] Setting up fresh environment...")
        
        try:
            # Create QApplication
            if not QApplication.instance():
                self.app = QApplication(sys.argv)
            else:
                self.app = QApplication.instance()
            
            # Clear any existing sequence to start fresh
            self.persistence_service = SequencePersistenceService()
            self.persistence_service.clear_current_sequence()
            
            print("✅ [WORKFLOW] Fresh environment setup complete")
            return True
            
        except Exception as e:
            print(f"❌ [WORKFLOW] Setup failed: {e}")
            return False
    
    def startup_program(self) -> bool:
        """Step 1: Start up the program"""
        print("🔄 [WORKFLOW] Step 1: Starting up the program...")
        
        try:
            from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget
            
            # Create fresh container and construct tab
            self.container = ApplicationFactory.create_production_app()
            self.construct_tab = ConstructTabWidget(self.container)
            
            # Get references
            if hasattr(self.construct_tab, 'layout_manager'):
                self.layout_manager = self.construct_tab.layout_manager
                if hasattr(self.layout_manager, 'workbench'):
                    self.workbench = self.layout_manager.workbench
            
            # Show UI
            self.construct_tab.show()
            self.construct_tab.resize(1200, 800)
            
            # Wait for startup to complete
            QTest.qWait(3000)
            
            # Log initial state
            self.log_workflow_state("PROGRAM_STARTUP")
            
            print("✅ [WORKFLOW] Step 1: Program started up")
            return True
            
        except Exception as e:
            print(f"❌ [WORKFLOW] Step 1 failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def select_start_position(self) -> bool:
        """Step 2: Select start position in start position picker"""
        print("🎯 [WORKFLOW] Step 2: Selecting start position...")
        
        try:
            # Log state before selecting start position
            self.log_workflow_state("BEFORE_START_POSITION_SELECT")
            
            # Find start position picker and select alpha1
            if self.layout_manager and hasattr(self.layout_manager, 'start_position_picker'):
                start_pos_picker = self.layout_manager.start_position_picker
                
                # Try to find alpha1 button and click it
                if hasattr(start_pos_picker, 'position_buttons'):
                    alpha1_button = start_pos_picker.position_buttons.get('alpha1')
                    if alpha1_button:
                        print("🖱️ [WORKFLOW] Clicking alpha1 start position...")
                        QTest.mouseClick(alpha1_button, 1)  # Left click
                        QTest.qWait(1000)  # Wait for processing
                        
                        self.log_workflow_state("AFTER_START_POSITION_SELECT")
                        print("✅ [WORKFLOW] Step 2: Start position selected")
                        return True
                    else:
                        print("❌ [WORKFLOW] Could not find alpha1 button")
                        return False
                else:
                    print("❌ [WORKFLOW] Start position picker has no position_buttons")
                    return False
            else:
                print("❌ [WORKFLOW] Could not find start position picker")
                return False
                
        except Exception as e:
            print(f"❌ [WORKFLOW] Step 2 failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def select_option_in_picker(self) -> bool:
        """Step 3: Select option in option picker"""
        print("⚙️ [WORKFLOW] Step 3: Selecting option in option picker...")
        
        try:
            # Log state before selecting option
            self.log_workflow_state("BEFORE_OPTION_SELECT")
            
            # Wait a moment for transition to option picker
            QTest.qWait(1000)
            
            # Find option picker and select an option
            if self.layout_manager and hasattr(self.layout_manager, 'option_picker'):
                option_picker = self.layout_manager.option_picker
                
                # Try to find and click the first available option
                if hasattr(option_picker, 'option_buttons'):
                    # Get first available option button
                    option_buttons = option_picker.option_buttons
                    if option_buttons:
                        first_option_key = list(option_buttons.keys())[0]
                        first_option_button = option_buttons[first_option_key]
                        
                        print(f"🖱️ [WORKFLOW] Clicking option: {first_option_key}")
                        QTest.mouseClick(first_option_button, 1)  # Left click
                        QTest.qWait(1000)  # Wait for processing
                        
                        self.log_workflow_state("AFTER_OPTION_SELECT")
                        print("✅ [WORKFLOW] Step 3: Option selected")
                        return True
                    else:
                        print("❌ [WORKFLOW] No option buttons available")
                        return False
                else:
                    print("❌ [WORKFLOW] Option picker has no option_buttons")
                    return False
            else:
                print("❌ [WORKFLOW] Could not find option picker")
                return False
                
        except Exception as e:
            print(f"❌ [WORKFLOW] Step 3 failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def click_clear_sequence_button(self) -> bool:
        """Step 4: Click Clear Sequence button"""
        print("🧹 [WORKFLOW] Step 4: Clicking Clear Sequence button...")
        
        try:
            # Log state before clearing
            self.log_workflow_state("BEFORE_CLEAR_BUTTON")
            
            # Find and click clear sequence button
            clear_button = self.find_clear_sequence_button()
            if clear_button:
                print("🖱️ [WORKFLOW] Clicking Clear Sequence button...")
                QTest.mouseClick(clear_button, 1)  # Left click
                
                # Monitor transitions after clear
                intervals = [100, 250, 500, 1000, 2000]
                for interval in intervals:
                    QTest.qWait(interval)
                    self.log_workflow_state(f"AFTER_CLEAR_+{interval}ms")
                
                print("✅ [WORKFLOW] Step 4: Clear Sequence button clicked")
                return True
            else:
                print("❌ [WORKFLOW] Could not find Clear Sequence button")
                return False
                
        except Exception as e:
            print(f"❌ [WORKFLOW] Step 4 failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def find_clear_sequence_button(self) -> QPushButton:
        """Find the clear sequence button"""
        # Search through all widgets for clear sequence button
        for widget in self.app.allWidgets():
            if isinstance(widget, QPushButton):
                # Check tooltip
                if hasattr(widget, 'toolTip') and 'clear' in widget.toolTip().lower():
                    return widget
                # Check text
                if hasattr(widget, 'text') and 'clear' in widget.text().lower():
                    return widget
                # Check object name
                if hasattr(widget, 'objectName') and 'clear' in widget.objectName().lower():
                    return widget
        return None
    
    def log_workflow_state(self, event: str):
        """Log the current workflow state"""
        picker_state = self.get_picker_state()
        sequence_state = self.get_sequence_state()
        timestamp = time.time()
        
        log_entry = {
            "timestamp": timestamp,
            "event": event,
            "picker_state": picker_state,
            "sequence_state": sequence_state
        }
        
        self.workflow_log.append(log_entry)
        print(f"🔍 [STATE] {event}: picker={picker_state}, sequence={sequence_state}")
    
    def get_picker_state(self) -> str:
        """Get the current picker state"""
        if not self.layout_manager or not hasattr(self.layout_manager, 'picker_stack'):
            return "no_picker_stack"
        
        picker_stack = self.layout_manager.picker_stack
        if not picker_stack:
            return "no_picker_stack_widget"
        
        current_index = picker_stack.currentIndex()
        widget_count = picker_stack.count()
        
        # Determine picker type
        if current_index == 0:
            return f"START_POSITION_PICKER(index_0_of_{widget_count})"
        elif current_index == 1:
            return f"OPTION_PICKER(index_1_of_{widget_count})"
        else:
            return f"UNKNOWN_PICKER(index_{current_index}_of_{widget_count})"
    
    def get_sequence_state(self) -> str:
        """Get the current sequence state"""
        try:
            sequence = self.persistence_service.load_current_sequence()
            return f"{len(sequence)}_items"
        except:
            return "unknown"
    
    def analyze_workflow_results(self):
        """Analyze the complete workflow results"""
        print("\n📊 [ANALYSIS] Complete User Workflow Analysis")
        print("=" * 70)
        
        if not self.workflow_log:
            print("❌ No workflow log data")
            return
        
        # Print detailed log
        for i, entry in enumerate(self.workflow_log):
            event = entry["event"]
            picker_state = entry["picker_state"]
            sequence_state = entry["sequence_state"]
            print(f"{i+1:2d}. {event:25s} → picker: {picker_state:30s} sequence: {sequence_state}")
        
        # Critical analysis
        print("\n🔍 [ANALYSIS] Critical Workflow Analysis:")
        
        # Check if we start with start position picker
        startup_entry = next((e for e in self.workflow_log if "STARTUP" in e["event"]), None)
        if startup_entry:
            if "START_POSITION_PICKER" in startup_entry["picker_state"]:
                print("✅ Program starts with start position picker")
            else:
                print(f"❌ Program starts with wrong picker: {startup_entry['picker_state']}")
        
        # Check transition to option picker after start position
        after_start_pos = next((e for e in self.workflow_log if "AFTER_START_POSITION_SELECT" in e["event"]), None)
        if after_start_pos:
            if "OPTION_PICKER" in after_start_pos["picker_state"]:
                print("✅ Correctly transitions to option picker after start position selection")
            else:
                print(f"❌ Wrong picker after start position: {after_start_pos['picker_state']}")
        
        # Check final state after clear
        final_entries = [e for e in self.workflow_log if "AFTER_CLEAR" in e["event"]]
        if final_entries:
            final_entry = final_entries[-1]  # Last entry
            if "START_POSITION_PICKER" in final_entry["picker_state"]:
                print("✅ CORRECT: Final state shows start position picker after clear")
            elif "OPTION_PICKER" in final_entry["picker_state"]:
                print("❌ BUG FOUND: Final state shows option picker after clear - THIS IS THE PROBLEM!")
            else:
                print(f"❓ Unclear final state: {final_entry['picker_state']}")
        
        # Check for unwanted transitions
        picker_states = [entry["picker_state"] for entry in self.workflow_log]
        transitions = []
        for i in range(1, len(picker_states)):
            if picker_states[i] != picker_states[i-1]:
                transitions.append((self.workflow_log[i-1]["event"], self.workflow_log[i]["event"], 
                                 picker_states[i-1], picker_states[i]))
        
        if transitions:
            print(f"\n🔄 Found {len(transitions)} picker transitions:")
            for from_event, to_event, from_state, to_state in transitions:
                print(f"   {from_event} → {to_event}")
                print(f"   {from_state} → {to_state}")
    
    def run_complete_workflow_test(self) -> bool:
        """Run the complete user workflow test"""
        print("🚀 COMPLETE USER WORKFLOW TEST")
        print("=" * 50)
        print("Testing the exact sequence that reveals the bug:")
        print("1. Start up program")
        print("2. Select start position")
        print("3. Select option")
        print("4. Click Clear Sequence")
        print("5. Verify correct picker state")
        print("=" * 50)
        
        test_steps = [
            ("Setup Fresh Environment", self.setup_fresh_environment),
            ("Step 1: Startup Program", self.startup_program),
            ("Step 2: Select Start Position", self.select_start_position),
            ("Step 3: Select Option", self.select_option_in_picker),
            ("Step 4: Click Clear Sequence", self.click_clear_sequence_button),
        ]
        
        for step_name, step_func in test_steps:
            print(f"\n🧪 {step_name}")
            print("-" * 40)
            
            try:
                success = step_func()
                if success:
                    print(f"✅ {step_name}: PASSED")
                else:
                    print(f"❌ {step_name}: FAILED")
                    return False
            except Exception as e:
                print(f"❌ {step_name}: ERROR - {e}")
                return False
        
        # Analyze results
        self.analyze_workflow_results()
        
        return True


def main():
    """Main test execution"""
    tester = CompleteUserWorkflowTester()
    success = tester.run_complete_workflow_test()
    
    if success:
        print("\n🎉 COMPLETE WORKFLOW TEST COMPLETED")
        print("✅ Check analysis above for the exact bug location")
        return 0
    else:
        print("\n❌ COMPLETE WORKFLOW TEST FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
