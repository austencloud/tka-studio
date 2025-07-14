#!/usr/bin/env python3
"""
Sequence Building with Fade Animation Test

This test simulates the real option picker workflow:
1. Start with a start position (e.g., alpha3)
2. Show options that start from alpha3
3. When user selects an option (e.g., alpha3 → beta5), add it to sequence
4. Show NEW options that start from beta5 (with fade transition)
5. Continue building sequence with visible fade animations

This properly demonstrates the fade animations during real usage.
"""

import sys
import time
from typing import List, Optional

# Add src to path for imports
sys.path.insert(0, "src")

from application.services.core.service_registration_manager import (
    ServiceRegistrationManager,
)
from application.services.ui.animation.modern_service_registration import (
    setup_modern_animation_services,
)
from core.dependency_injection.di_container import DIContainer
from domain.models.beat_data import BeatData
from domain.models.sequence_data import SequenceData
from presentation.components.option_picker.components.option_picker import OptionPicker
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SequenceBuildingTest(QMainWindow):
    """Test sequence building with fade animations."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sequence Building with Fade Animation Test")
        self.setGeometry(100, 100, 1600, 1000)

        # Initialize services
        self.setup_services()

        # Sequence building state
        self.current_sequence = SequenceData()
        self.current_end_position = "alpha3"  # Start position
        self.available_positions = self.load_available_positions()

        # Performance tracking
        self.transition_times = []

        # Initialize UI attributes
        self.log_display = None

        # Setup UI
        self.setup_ui()

        # Start with initial options
        QTimer.singleShot(1000, self.load_initial_options)

    def setup_services(self):
        """Setup DI container with all required services."""
        try:
            self.container = DIContainer()

            # Register animation services
            setup_modern_animation_services(self.container)

            # Register all application services
            registration_manager = ServiceRegistrationManager()
            registration_manager.register_all_services(self.container)

            self.services_available = True
            print("✅ All services registered successfully")

        except Exception as e:
            self.services_available = False
            print(f"❌ Service setup failed: {e}")
            import traceback

            traceback.print_exc()

    def load_available_positions(self) -> List[str]:
        """Load all available start/end positions from CSV."""
        positions = set()
        try:
            from application.services.pictograph.pictograph_csv_manager import (
                PictographCSVManager,
            )

            csv_manager = PictographCSVManager()
            csv_data = csv_manager._load_csv_data()

            if not csv_data.empty:
                # Get all unique start and end positions
                if "start_pos" in csv_data.columns:
                    positions.update(csv_data["start_pos"].dropna().unique())
                if "end_pos" in csv_data.columns:
                    positions.update(csv_data["end_pos"].dropna().unique())

            positions_list = sorted(list(positions))
            print(
                f"✅ Loaded {len(positions_list)} available positions: {positions_list[:10]}..."
            )
            return positions_list

        except Exception as e:
            print(f"❌ Failed to load positions: {e}")
            return [
                "alpha1",
                "alpha3",
                "alpha5",
                "beta3",
                "beta5",
                "gamma1",
                "gamma3",
                "gamma5",
            ]

    def setup_ui(self):
        """Setup the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main horizontal layout
        main_layout = QHBoxLayout(central_widget)

        # Left side: Option picker (2/3 width)
        self.setup_option_picker_side(main_layout)

        # Right side: Sequence building controls (1/3 width)
        self.setup_sequence_building_side(main_layout)

    def setup_option_picker_side(self, main_layout):
        """Setup the option picker display side."""
        picker_container = QGroupBox("Option Picker - Real Sequence Building")
        picker_container.setMinimumWidth(1000)
        main_layout.addWidget(picker_container, 2)

        picker_layout = QVBoxLayout(picker_container)

        # Current state display
        self.state_label = QLabel("Current End Position: alpha3 (Start Position)")
        self.state_label.setStyleSheet(
            "background: #e3f2fd; padding: 8px; border-radius: 4px; font-weight: bold;"
        )
        picker_layout.addWidget(self.state_label)

        # Animation status
        self.animation_status = QLabel(
            "🎭 Animations: Enabled (200ms fade transitions)"
        )
        self.animation_status.setStyleSheet(
            "color: green; font-weight: bold; padding: 4px;"
        )
        picker_layout.addWidget(self.animation_status)

        # Create option picker
        try:
            if self.services_available:
                self.option_picker = OptionPicker(
                    container=self.container,
                    progress_callback=self.progress_callback,
                    parent=picker_container,
                )

                # Initialize the option picker
                self.option_picker.initialize()

                # Add to layout
                picker_layout.addWidget(self.option_picker.get_widget())

                # Connect signals
                self.option_picker.pictograph_selected.connect(
                    self.on_pictograph_selected
                )

                print("✅ Option picker created successfully")

            else:
                error_label = QLabel(
                    "❌ Services not available - cannot create option picker"
                )
                error_label.setStyleSheet("color: red;")
                picker_layout.addWidget(error_label)

        except Exception as e:
            error_label = QLabel(f"❌ Failed to create option picker: {e}")
            error_label.setStyleSheet("color: red;")
            picker_layout.addWidget(error_label)
            print(f"Option picker creation failed: {e}")

    def setup_sequence_building_side(self, main_layout):
        """Setup the sequence building controls side."""
        control_container = QGroupBox("Sequence Building & Controls")
        control_container.setMinimumWidth(500)
        main_layout.addWidget(control_container, 1)

        control_layout = QVBoxLayout(control_container)

        # Current sequence display
        self.setup_sequence_display(control_layout)

        # Position controls
        self.setup_position_controls(control_layout)

        # Animation controls
        self.setup_animation_controls(control_layout)

        # Performance display
        self.setup_performance_display(control_layout)

        # Log display
        self.setup_log_display(control_layout)

    def setup_sequence_display(self, layout):
        """Setup current sequence display."""
        seq_group = QGroupBox("Current Sequence")
        layout.addWidget(seq_group)

        seq_layout = QVBoxLayout(seq_group)

        self.sequence_list = QListWidget()
        self.sequence_list.setMaximumHeight(150)
        seq_layout.addWidget(self.sequence_list)

        # Sequence controls
        seq_controls = QHBoxLayout()

        self.clear_sequence_button = QPushButton("🗑️ Clear Sequence")
        self.clear_sequence_button.clicked.connect(self.clear_sequence)
        seq_controls.addWidget(self.clear_sequence_button)

        self.undo_last_button = QPushButton("↶ Undo Last")
        self.undo_last_button.clicked.connect(self.undo_last_beat)
        seq_controls.addWidget(self.undo_last_button)

        seq_layout.addLayout(seq_controls)

    def setup_position_controls(self, layout):
        """Setup position selection controls."""
        pos_group = QGroupBox("Quick Position Jump")
        layout.addWidget(pos_group)

        pos_layout = QVBoxLayout(pos_group)

        # Quick position buttons
        pos_buttons = QHBoxLayout()

        for pos in ["alpha1", "alpha3", "alpha5", "beta3", "beta5", "gamma3"]:
            btn = QPushButton(pos)
            btn.clicked.connect(lambda checked, p=pos: self.jump_to_position(p))
            pos_buttons.addWidget(btn)

        pos_layout.addLayout(pos_buttons)

        # Custom position input
        custom_layout = QHBoxLayout()
        self.custom_position_input = QLabel("Enter position manually if needed")
        custom_layout.addWidget(self.custom_position_input)
        pos_layout.addLayout(custom_layout)

    def setup_animation_controls(self, layout):
        """Setup animation controls."""
        anim_group = QGroupBox("Animation Controls")
        layout.addWidget(anim_group)

        anim_layout = QVBoxLayout(anim_group)

        self.toggle_animation_button = QPushButton(
            "🎭 Disable Animations (Test Direct Mode)"
        )
        self.toggle_animation_button.clicked.connect(self.toggle_animation_mode)
        anim_layout.addWidget(self.toggle_animation_button)

        self.force_refresh_button = QPushButton("🔄 Force Refresh (Test Fade)")
        self.force_refresh_button.clicked.connect(self.force_refresh_options)
        anim_layout.addWidget(self.force_refresh_button)

    def setup_performance_display(self, layout):
        """Setup performance monitoring."""
        perf_group = QGroupBox("Performance Metrics")
        layout.addWidget(perf_group)

        perf_layout = QVBoxLayout(perf_group)

        self.performance_label = QLabel(
            "Transitions: 0\nLast: N/A\nAvg: N/A\nTarget: 200ms"
        )
        self.performance_label.setFont(QFont("Courier", 9))
        perf_layout.addWidget(self.performance_label)

    def setup_log_display(self, layout):
        """Setup log display."""
        log_group = QGroupBox("Activity Log")
        layout.addWidget(log_group)

        log_layout = QVBoxLayout(log_group)

        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(150)
        self.log_display.setFont(QFont("Courier", 8))
        log_layout.addWidget(self.log_display)

        clear_button = QPushButton("Clear Log")
        clear_button.clicked.connect(self.log_display.clear)
        log_layout.addWidget(clear_button)

    def progress_callback(self, message: str, progress: float):
        """Progress callback for option picker."""
        self.log(f"Progress: {message} ({progress:.1%})")

    def log(self, message: str):
        """Add message to log display."""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"

        print(log_message)

        if self.log_display:
            self.log_display.append(log_message)
            scrollbar = self.log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def load_initial_options(self):
        """Load initial options for the start position."""
        self.log(f"Loading initial options for position: {self.current_end_position}")
        self.load_options_for_position(self.current_end_position)

    def load_options_for_position(self, start_position: str):
        """Load options that start from the given position using proper sequence refresh."""
        try:
            # Use the CURRENT sequence state to trigger proper option loading
            # This is the key - we need to refresh based on the current sequence, not create a new one

            # Measure performance
            start_time = time.perf_counter()

            # Use the proper option picker refresh method with current sequence
            # This will trigger the real option loading logic with fade animations
            self.option_picker.refresh_options_from_modern_sequence(
                self.current_sequence
            )

            # Record timing
            transition_time = (time.perf_counter() - start_time) * 1000
            self.transition_times.append(transition_time)

            # Update performance display
            self.update_performance_display(transition_time)

            # Update state display
            self.state_label.setText(
                f"Current End Position: {start_position} → Showing options that START from {start_position}"
            )

            self.log(
                f"Refreshed options for current sequence ending at {start_position} - {transition_time:.1f}ms"
            )

        except Exception as e:
            self.log(f"Failed to load options for {start_position}: {e}")
            import traceback

            traceback.print_exc()

    def create_sequence_ending_at(self, end_position: str) -> SequenceData:
        """Create a sequence that ends at the given position."""
        try:
            from application.services.data.pictograph_factory import PictographFactory
            from application.services.pictograph.pictograph_csv_manager import (
                PictographCSVManager,
            )

            csv_manager = PictographCSVManager()
            pictograph_factory = PictographFactory()
            csv_data = csv_manager._load_csv_data()

            # Find any pictograph that starts from the target position
            matching_entries = csv_data[csv_data["start_pos"] == end_position]

            if not matching_entries.empty:
                entry = matching_entries.iloc[0].to_dict()

                # Create pictograph data
                pictograph_data = pictograph_factory.create_pictograph_data_from_entry(
                    entry, "diamond"
                )

                # Create beat
                beat = BeatData(
                    beat_number=len(self.current_sequence.beats) + 1,
                    pictograph_data=pictograph_data,
                )

                # Create sequence with this beat
                sequence = SequenceData()
                sequence.add_beat(beat)

                return sequence

            # Fallback: create empty sequence
            return SequenceData()

        except Exception as e:
            self.log(f"Error creating sequence ending at {end_position}: {e}")
            return SequenceData()

    def on_pictograph_selected(self, pictograph_data):
        """Handle pictograph selection - this is where the magic happens!"""
        try:
            letter = pictograph_data.letter
            # Get start and end positions from the selected pictograph
            start_pos = getattr(pictograph_data, "start_position", "unknown")
            end_pos = getattr(pictograph_data, "end_position", "unknown")

            self.log(f"🎯 SELECTED: {letter} pictograph ({start_pos} → {end_pos})")

            # Add to current sequence (SequenceData.add_beat returns a NEW sequence - immutable pattern!)
            beat = BeatData(
                beat_number=len(self.current_sequence.beats) + 1,
                pictograph_data=pictograph_data,
            )
            self.current_sequence = self.current_sequence.add_beat(
                beat
            )  # ← UPDATE REFERENCE!

            # Update sequence display
            self.update_sequence_display()

            # Update current end position
            self.current_end_position = end_pos

            # NOW trigger the option picker refresh with the UPDATED sequence
            # This is the key - refresh with the new sequence state to show new options
            self.log(f"🔄 Refreshing options with updated sequence (FADE ANIMATION)")

            # Measure performance for the fade transition
            start_time = time.perf_counter()

            # Refresh option picker with the updated sequence - this should trigger fade animations
            self.option_picker.refresh_options_from_modern_sequence(
                self.current_sequence
            )

            # Record timing
            transition_time = (time.perf_counter() - start_time) * 1000
            self.transition_times.append(transition_time)
            self.update_performance_display(transition_time)

            # Update state display
            self.state_label.setText(
                f"Sequence updated! Next options will start from: {end_pos}"
            )

            self.log(
                f"✅ Options refreshed with fade animation - {transition_time:.1f}ms"
            )

        except Exception as e:
            self.log(f"Error handling pictograph selection: {e}")
            import traceback

            traceback.print_exc()

    def update_sequence_display(self):
        """Update the sequence display list."""
        self.sequence_list.clear()

        for i, beat in enumerate(self.current_sequence.beats):
            if beat.pictograph_data:
                letter = beat.pictograph_data.letter
                start_pos = getattr(beat.pictograph_data, "start_position", "?")
                end_pos = getattr(beat.pictograph_data, "end_position", "?")

                item_text = f"Beat {i+1}: {letter} ({start_pos} → {end_pos})"
                item = QListWidgetItem(item_text)
                self.sequence_list.addItem(item)

    def update_performance_display(self, last_time: float):
        """Update performance metrics display."""
        avg_time = (
            sum(self.transition_times) / len(self.transition_times)
            if self.transition_times
            else 0
        )
        target_time = 200

        status = "✅" if last_time <= target_time * 1.5 else "⚠️"

        self.performance_label.setText(
            f"Transitions: {len(self.transition_times)}\n"
            f"Last: {last_time:.1f}ms\n"
            f"Avg: {avg_time:.1f}ms\n"
            f"Target: {target_time}ms {status}"
        )

    def clear_sequence(self):
        """Clear the current sequence and reset."""
        self.current_sequence = SequenceData()
        self.current_end_position = "alpha3"
        self.update_sequence_display()
        self.log("🗑️ Sequence cleared - reset to alpha3")
        self.load_options_for_position(self.current_end_position)

    def undo_last_beat(self):
        """Remove the last beat from sequence."""
        if self.current_sequence.beats:
            removed_beat = self.current_sequence.beats.pop()

            # Update end position to previous beat's end position
            if self.current_sequence.beats:
                last_beat = self.current_sequence.beats[-1]
                if last_beat.pictograph_data:
                    self.current_end_position = getattr(
                        last_beat.pictograph_data, "end_position", "alpha3"
                    )
            else:
                self.current_end_position = "alpha3"

            self.update_sequence_display()
            self.log(f"↶ Undid last beat - back to {self.current_end_position}")
            self.load_options_for_position(self.current_end_position)

    def jump_to_position(self, position: str):
        """Jump to a specific position."""
        self.current_end_position = position
        self.log(f"🎯 Jumped to position: {position}")
        self.load_options_for_position(position)

    def toggle_animation_mode(self):
        """Toggle animation mode."""
        if not hasattr(self, "option_picker"):
            return

        try:
            scroll_widget = self.option_picker.option_picker_widget.option_picker_scroll

            if (
                hasattr(scroll_widget, "_animation_orchestrator")
                and scroll_widget._animation_orchestrator
            ):
                scroll_widget._animation_orchestrator = None
                self.toggle_animation_button.setText("🎭 Enable Animations")
                self.animation_status.setText("🚫 Animations: Disabled (Direct Mode)")
                self.animation_status.setStyleSheet(
                    "color: red; font-weight: bold; padding: 4px;"
                )
                self.log("🚫 Animations DISABLED - direct updates only")
            else:
                from core.interfaces.animation_core_interfaces import (
                    IAnimationOrchestrator,
                )

                scroll_widget._animation_orchestrator = self.container.resolve(
                    IAnimationOrchestrator
                )
                self.toggle_animation_button.setText(
                    "🎭 Disable Animations (Test Direct Mode)"
                )
                self.animation_status.setText(
                    "🎭 Animations: Enabled (200ms fade transitions)"
                )
                self.animation_status.setStyleSheet(
                    "color: green; font-weight: bold; padding: 4px;"
                )
                self.log("🎭 Animations ENABLED - fade transitions active")

        except Exception as e:
            self.log(f"Failed to toggle animation mode: {e}")

    def force_refresh_options(self):
        """Force refresh current options to test fade animation."""
        self.log(f"🔄 Force refreshing options - this should show fade animation")

        # Measure performance for the fade transition
        start_time = time.perf_counter()

        # Force refresh with current sequence - this should trigger visible fade
        self.option_picker.refresh_options_from_modern_sequence(self.current_sequence)

        # Record timing
        transition_time = (time.perf_counter() - start_time) * 1000
        self.transition_times.append(transition_time)
        self.update_performance_display(transition_time)

        self.log(
            f"✅ Force refresh completed with fade animation - {transition_time:.1f}ms"
        )


def main():
    """Run the sequence building test."""
    app = QApplication(sys.argv)

    print("🎯 Sequence Building with Fade Animation Test")
    print("=" * 55)
    print("This test simulates REAL option picker usage:")
    print("• Start from a position (alpha3)")
    print("• Click pictographs to build sequence")
    print("• See fade animations when new options load")
    print("• Build logical sequences with position continuity")
    print("• Compare animated vs direct update modes")
    print()

    test_window = SequenceBuildingTest()
    test_window.show()

    print("🚀 Sequence building test launched!")
    print("Instructions:")
    print("1. Click any pictograph in the option picker")
    print("2. Watch fade animation as NEW options load")
    print("3. Continue clicking to build a sequence")
    print("4. Use controls to jump positions, toggle animations")
    print("5. Monitor performance metrics")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
