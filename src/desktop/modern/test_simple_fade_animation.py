#!/usr/bin/env python3
"""
Simple Fade Animation Test

This test focuses ONLY on demonstrating the fade animations by:
1. Creating a minimal option picker setup
2. Manually triggering different option loads
3. Showing visible fade transitions
4. Avoiding complex service dependencies
"""

import sys
import time
from typing import List

# Add src to path for imports
sys.path.insert(0, "src")

from application.services.ui.animation.modern_service_registration import (
    setup_modern_animation_services,
)
from core.dependency_injection.di_container import DIContainer
from domain.models.beat_data import BeatData
from domain.models.sequence_data import SequenceData
from presentation.components.option_picker.components.option_picker import OptionPicker
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SimpleFadeTest(QMainWindow):
    """Simple test focused only on fade animations."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Fade Animation Test")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize minimal services
        self.setup_minimal_services()

        # Test sequences
        self.test_sequences = []
        self.current_index = 0

        # Setup UI
        self.setup_ui()

        # Create test sequences
        QTimer.singleShot(1000, self.create_test_sequences)

    def setup_minimal_services(self):
        """Setup only the minimal services needed for option picker + animations."""
        try:
            self.container = DIContainer()

            # Register animation services
            setup_modern_animation_services(self.container)

            # Register only essential services for option picker
            from application.services.data.pictograph_factory import PictographFactory
            from application.services.option_picker.option_configuration_service import (
                OptionConfigurationService,
            )
            from application.services.option_picker.sequence_option_service import (
                SequenceOptionService,
            )
            from application.services.pictograph.pictograph_csv_manager import (
                PictographCSVManager,
            )
            from application.services.positioning.arrows.utilities.pictograph_position_matcher import (
                PictographPositionMatcher,
            )

            # Register essential services
            self.container.register_singleton(
                PictographCSVManager, PictographCSVManager
            )
            self.container.register_singleton(PictographFactory, PictographFactory)

            # Register position matcher class
            self.container.register_singleton(
                PictographPositionMatcher, PictographPositionMatcher
            )

            # Register sequence option service
            position_matcher = self.container.resolve(PictographPositionMatcher)
            sequence_option_service = SequenceOptionService(position_matcher)
            self.container.register_singleton(
                SequenceOptionService, lambda: sequence_option_service
            )

            # Register config service
            config_service = OptionConfigurationService()
            self.container.register_singleton(
                OptionConfigurationService, lambda: config_service
            )

            self.services_available = True
            print("✅ Minimal services registered successfully")

        except Exception as e:
            self.services_available = False
            print(f"❌ Minimal service setup failed: {e}")
            import traceback

            traceback.print_exc()

    def setup_ui(self):
        """Setup the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("🎭 Simple Fade Animation Test")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2196F3; padding: 10px;")
        main_layout.addWidget(title)

        # Status
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet(
            "background: #f5f5f5; padding: 8px; border-radius: 4px;"
        )
        main_layout.addWidget(self.status_label)

        # Controls
        controls_layout = QHBoxLayout()

        self.load_sequence_1_btn = QPushButton("Load Sequence 1 (alpha1 options)")
        self.load_sequence_1_btn.clicked.connect(lambda: self.load_sequence(0))
        controls_layout.addWidget(self.load_sequence_1_btn)

        self.load_sequence_2_btn = QPushButton("Load Sequence 2 (beta3 options)")
        self.load_sequence_2_btn.clicked.connect(lambda: self.load_sequence(1))
        controls_layout.addWidget(self.load_sequence_2_btn)

        self.load_sequence_3_btn = QPushButton("Load Sequence 3 (gamma7 options)")
        self.load_sequence_3_btn.clicked.connect(lambda: self.load_sequence(2))
        controls_layout.addWidget(self.load_sequence_3_btn)

        main_layout.addLayout(controls_layout)

        # Option picker container
        picker_container = QGroupBox("Option Picker - Watch for Fade Transitions")
        main_layout.addWidget(picker_container)

        picker_layout = QVBoxLayout(picker_container)

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

                self.status_label.setText(
                    "✅ Option picker ready - Click buttons to see fade transitions"
                )

            else:
                error_label = QLabel("❌ Services not available")
                error_label.setStyleSheet("color: red;")
                picker_layout.addWidget(error_label)

        except Exception as e:
            error_label = QLabel(f"❌ Failed to create option picker: {e}")
            error_label.setStyleSheet("color: red;")
            picker_layout.addWidget(error_label)
            print(f"Option picker creation failed: {e}")

    def progress_callback(self, message: str, progress: float):
        """Progress callback for option picker."""
        print(f"Progress: {message} ({progress:.1%})")

    def create_test_sequences(self):
        """Create test sequences that end at different positions."""
        try:
            from application.services.data.pictograph_factory import PictographFactory
            from application.services.pictograph.pictograph_csv_manager import (
                PictographCSVManager,
            )

            csv_manager = PictographCSVManager()
            pictograph_factory = PictographFactory()
            csv_data = csv_manager._load_csv_data()

            # Create sequences ending at different positions to show different options
            target_positions = ["alpha1", "beta3", "gamma7"]

            for target_pos in target_positions:
                # Find a pictograph that ends at this position
                matching_entries = csv_data[csv_data["end_pos"] == target_pos]

                if not matching_entries.empty:
                    entry = matching_entries.iloc[0].to_dict()

                    # Create pictograph data
                    pictograph_data = (
                        pictograph_factory.create_pictograph_data_from_entry(
                            entry, "diamond"
                        )
                    )

                    # Create beat
                    beat = BeatData(beat_number=1, pictograph_data=pictograph_data)

                    # Create sequence
                    sequence = SequenceData()
                    sequence = sequence.add_beat(beat)

                    self.test_sequences.append(sequence)

                    print(f"✅ Created test sequence ending at {target_pos}")

            self.status_label.setText(
                f"✅ Created {len(self.test_sequences)} test sequences - Ready for fade testing!"
            )

        except Exception as e:
            print(f"❌ Failed to create test sequences: {e}")
            import traceback

            traceback.print_exc()

    def load_sequence(self, index: int):
        """Load a specific test sequence to trigger fade animation."""
        if not self.test_sequences or index >= len(self.test_sequences):
            print(f"❌ No sequence available at index {index}")
            return

        try:
            sequence = self.test_sequences[index]

            # Get the end position for display
            if sequence.beats and sequence.beats[-1].pictograph_data:
                end_pos = getattr(
                    sequence.beats[-1].pictograph_data, "end_position", "unknown"
                )
            else:
                end_pos = "unknown"

            print(f"🔄 Loading sequence {index + 1} ending at {end_pos}")
            self.status_label.setText(
                f"🔄 Loading sequence {index + 1} ending at {end_pos} - Watch for fade animation!"
            )

            # Measure performance
            start_time = time.perf_counter()

            # Trigger the option picker refresh - this should show fade animation
            self.option_picker.refresh_options_from_modern_sequence(sequence)

            # Record timing
            transition_time = (time.perf_counter() - start_time) * 1000

            print(f"✅ Sequence {index + 1} loaded - {transition_time:.1f}ms")
            self.status_label.setText(
                f"✅ Sequence {index + 1} loaded ({transition_time:.1f}ms) - Options now show pictographs starting from {end_pos}"
            )

        except Exception as e:
            print(f"❌ Failed to load sequence {index}: {e}")
            import traceback

            traceback.print_exc()


def main():
    """Run the simple fade test."""
    app = QApplication(sys.argv)

    print("🎭 Simple Fade Animation Test")
    print("=" * 40)
    print("This test demonstrates fade animations by:")
    print("• Creating sequences ending at different positions")
    print("• Loading different option sets")
    print("• Showing fade transitions between option sets")
    print("• Minimal service dependencies")
    print()

    test_window = SimpleFadeTest()
    test_window.show()

    print("🚀 Simple fade test launched!")
    print("Click the buttons to load different sequences and see fade animations!")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
