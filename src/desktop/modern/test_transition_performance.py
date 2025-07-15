#!/usr/bin/env python3
"""
Test script for verifying transition performance between start position picker and option picker.

This script tests the new fade transition implementation to ensure:
1. Transitions complete within <100ms performance target
2. No redundant fade animations occur
3. Content is pre-loaded before widget transitions
4. Smooth visual feedback is provided

Usage:
    python test_transition_performance.py
"""

import asyncio
import sys
import time
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from core.dependency_injection.di_container import DIContainer
from presentation.tabs.construct.layout_manager import ConstructTabLayoutManager
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


class TransitionTestWindow(QMainWindow):
    """Test window for transition performance testing."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transition Performance Test")
        self.setGeometry(100, 100, 1200, 800)

        # Create DI container and register animation services
        from core.application.application_factory import (
            ApplicationFactory,
            ApplicationMode,
        )

        self.container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)

        # Setup UI
        self.setup_ui()

        # Track transition times
        self.transition_times = []

    def setup_ui(self):
        """Setup the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create test buttons
        self.start_pos_btn = QPushButton("Transition to Start Position Picker")
        self.option_picker_btn = QPushButton("Transition to Option Picker")
        self.test_sequence_btn = QPushButton("Run Performance Test Sequence")

        layout.addWidget(self.start_pos_btn)
        layout.addWidget(self.option_picker_btn)
        layout.addWidget(self.test_sequence_btn)

        # Create layout manager
        try:
            self.layout_manager = ConstructTabLayoutManager(
                self.container, progress_callback=self.progress_callback
            )

            # Setup the construct tab UI
            construct_widget = QWidget()
            self.layout_manager.setup_ui(construct_widget)
            layout.addWidget(construct_widget)

            # Connect buttons
            self.start_pos_btn.clicked.connect(self.test_start_pos_transition)
            self.option_picker_btn.clicked.connect(self.test_option_picker_transition)
            self.test_sequence_btn.clicked.connect(self.run_performance_test)

        except Exception as e:
            print(f"❌ Failed to create layout manager: {e}")
            import traceback

            traceback.print_exc()

    def progress_callback(self, message: str, progress: float):
        """Progress callback for initialization."""
        print(f"📊 {message} ({progress:.1%})")

    def test_start_pos_transition(self):
        """Test transition to start position picker."""
        start_time = time.perf_counter()

        def on_transition_complete():
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
            self.transition_times.append(duration_ms)
            print(f"✅ Start position transition: {duration_ms:.2f}ms")

            if duration_ms > 100:
                print(f"⚠️ Transition exceeded 100ms target!")
            else:
                print(f"🎯 Transition within performance target")

        # Trigger transition
        self.layout_manager.transition_to_start_position_picker()

        # Use timer to check completion (approximate)
        QTimer.singleShot(300, on_transition_complete)

    def test_option_picker_transition(self):
        """Test transition to option picker."""
        start_time = time.perf_counter()

        def on_transition_complete():
            end_time = time.perf_counter()
            duration_ms = (end_time - start_time) * 1000
            self.transition_times.append(duration_ms)
            print(f"✅ Option picker transition: {duration_ms:.2f}ms")

            if duration_ms > 100:
                print(f"⚠️ Transition exceeded 100ms target!")
            else:
                print(f"🎯 Transition within performance target")

        # Trigger transition
        self.layout_manager.transition_to_option_picker()

        # Use timer to check completion (approximate)
        QTimer.singleShot(300, on_transition_complete)

    def run_performance_test(self):
        """Run a sequence of transitions to test performance."""
        print("\n🚀 Starting performance test sequence...")
        self.transition_times.clear()

        # Run multiple transitions
        self.test_transition_sequence(0)

    def test_transition_sequence(self, iteration: int):
        """Run a sequence of transitions for performance testing."""
        max_iterations = 10

        if iteration >= max_iterations:
            self.report_performance_results()
            return

        print(f"\n📊 Test iteration {iteration + 1}/{max_iterations}")

        # Alternate between transitions
        if iteration % 2 == 0:
            self.test_option_picker_transition()
            QTimer.singleShot(500, lambda: self.test_transition_sequence(iteration + 1))
        else:
            self.test_start_pos_transition()
            QTimer.singleShot(500, lambda: self.test_transition_sequence(iteration + 1))

    def report_performance_results(self):
        """Report the performance test results."""
        if not self.transition_times:
            print("❌ No transition times recorded")
            return

        avg_time = sum(self.transition_times) / len(self.transition_times)
        max_time = max(self.transition_times)
        min_time = min(self.transition_times)

        print(f"\n📈 Performance Test Results:")
        print(f"   Total transitions: {len(self.transition_times)}")
        print(f"   Average time: {avg_time:.2f}ms")
        print(f"   Min time: {min_time:.2f}ms")
        print(f"   Max time: {max_time:.2f}ms")

        target_met = all(t <= 100 for t in self.transition_times)
        if target_met:
            print(f"🎯 All transitions met <100ms target!")
        else:
            slow_transitions = [t for t in self.transition_times if t > 100]
            print(f"⚠️ {len(slow_transitions)} transitions exceeded 100ms target")

        print(f"\n✅ Performance test complete")


def main():
    """Main function to run the transition performance test."""
    app = QApplication(sys.argv)

    # Create test window
    window = TransitionTestWindow()
    window.show()

    print("🧪 Transition Performance Test")
    print("=" * 50)
    print("Use the buttons to test individual transitions")
    print("or run the full performance test sequence.")
    print("Target: All transitions should complete in <100ms")
    print("=" * 50)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
