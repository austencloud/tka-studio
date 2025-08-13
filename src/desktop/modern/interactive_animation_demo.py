"""
Interactive Animation Demo with Real Pictographs
Showcases the modern animation system with actual TKA pictograph data.
"""

from __future__ import annotations

import asyncio
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


# Add src to path for imports
sys.path.insert(0, "src")

from desktop.modern.application.services.data.pictograph_factory import (
    PictographFactory,
)
from desktop.modern.application.services.pictograph.pictograph_csv_manager import (
    PictographCSVManager,
)
from desktop.modern.application.services.ui.animation.modern_service_registration import (
    setup_modern_animation_services,
)
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.animation_core_interfaces import (
    AnimationConfig,
    EasingType,
    IAnimationOrchestrator,
)
from desktop.modern.presentation.components.pictograph.pictograph_widget import (
    PictographWidget,
)


class InteractiveAnimationDemo(QMainWindow):
    """Interactive demo showcasing animation system with real pictographs."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎭 TKA Animation System Demo - Interactive Pictographs")
        self.setGeometry(100, 100, 1400, 900)

        # Initialize services
        self.container = DIContainer()
        setup_modern_animation_services(self.container)
        self.animator: IAnimationOrchestrator = self.container.resolve(
            IAnimationOrchestrator
        )

        # Initialize pictograph services
        self.csv_manager = PictographCSVManager()
        self.pictograph_factory = PictographFactory()

        # Store pictographs and their components
        self.pictographs: list[PictographWidget] = []
        self.current_pictograph_index = 0

        # Animation state
        self.animation_duration = 0.5
        self.current_easing = EasingType.EASE_IN_OUT

        self.setup_ui()
        self.create_sample_pictographs()

    def setup_ui(self):
        """Setup the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # Left panel - Controls
        controls_panel = self.create_controls_panel()
        main_layout.addWidget(controls_panel, 1)

        # Right panel - Pictograph display area
        display_panel = self.create_display_panel()
        main_layout.addWidget(display_panel, 3)

    def create_controls_panel(self) -> QWidget:
        """Create the controls panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Title
        title = QLabel("🎭 Animation Controls")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Basic Animation Controls
        basic_group = QGroupBox("Basic Animations")
        basic_layout = QVBoxLayout(basic_group)

        fade_in_btn = QPushButton("Fade In Current")
        fade_in_btn.clicked.connect(
            lambda: asyncio.create_task(self.fade_current_pictograph(True))
        )
        basic_layout.addWidget(fade_in_btn)

        fade_out_btn = QPushButton("Fade Out Current")
        fade_out_btn.clicked.connect(
            lambda: asyncio.create_task(self.fade_current_pictograph(False))
        )
        basic_layout.addWidget(fade_out_btn)

        layout.addWidget(basic_group)

        # Cross-Fade Controls
        crossfade_group = QGroupBox("Cross-Fade Animations")
        crossfade_layout = QVBoxLayout(crossfade_group)

        next_btn = QPushButton("Cross-Fade to Next")
        next_btn.clicked.connect(lambda: asyncio.create_task(self.crossfade_to_next()))
        crossfade_layout.addWidget(next_btn)

        prev_btn = QPushButton("Cross-Fade to Previous")
        prev_btn.clicked.connect(
            lambda: asyncio.create_task(self.crossfade_to_previous())
        )
        crossfade_layout.addWidget(prev_btn)

        layout.addWidget(crossfade_group)

        # Movement Controls
        movement_group = QGroupBox("Movement Animations")
        movement_layout = QGridLayout(movement_group)

        move_up_btn = QPushButton("↑ Move Up")
        move_up_btn.clicked.connect(
            lambda: asyncio.create_task(self.move_pictograph(0, -50))
        )
        movement_layout.addWidget(move_up_btn, 0, 1)

        move_left_btn = QPushButton("← Move Left")
        move_left_btn.clicked.connect(
            lambda: asyncio.create_task(self.move_pictograph(-50, 0))
        )
        movement_layout.addWidget(move_left_btn, 1, 0)

        move_right_btn = QPushButton("Move Right →")
        move_right_btn.clicked.connect(
            lambda: asyncio.create_task(self.move_pictograph(50, 0))
        )
        movement_layout.addWidget(move_right_btn, 1, 2)

        move_down_btn = QPushButton("↓ Move Down")
        move_down_btn.clicked.connect(
            lambda: asyncio.create_task(self.move_pictograph(0, 50))
        )
        movement_layout.addWidget(move_down_btn, 2, 1)

        center_btn = QPushButton("🎯 Center")
        center_btn.clicked.connect(
            lambda: asyncio.create_task(self.center_pictograph())
        )
        movement_layout.addWidget(center_btn, 1, 1)

        layout.addWidget(movement_group)

        # Animation Settings
        settings_group = QGroupBox("Animation Settings")
        settings_layout = QVBoxLayout(settings_group)

        # Duration slider
        duration_label = QLabel(f"Duration: {self.animation_duration:.1f}s")
        settings_layout.addWidget(duration_label)

        duration_slider = QSlider(Qt.Orientation.Horizontal)
        duration_slider.setRange(1, 30)  # 0.1s to 3.0s
        duration_slider.setValue(int(self.animation_duration * 10))
        duration_slider.valueChanged.connect(
            lambda v: self.update_duration(v / 10.0, duration_label)
        )
        settings_layout.addWidget(duration_slider)

        # Easing selection
        easing_label = QLabel("Easing:")
        settings_layout.addWidget(easing_label)

        easing_combo = QComboBox()
        easing_combo.addItems(
            ["Linear", "Ease In-Out", "Ease In", "Ease Out", "Spring"]
        )
        easing_combo.setCurrentText("Ease In-Out")
        easing_combo.currentTextChanged.connect(self.update_easing)
        settings_layout.addWidget(easing_combo)

        layout.addWidget(settings_group)

        # Advanced Controls
        advanced_group = QGroupBox("Advanced Features")
        advanced_layout = QVBoxLayout(advanced_group)

        undo_btn = QPushButton("↶ Undo Last Animation")
        undo_btn.clicked.connect(lambda: asyncio.create_task(self.undo_animation()))
        advanced_layout.addWidget(undo_btn)

        sequence_btn = QPushButton("🎬 Play Sequence")
        sequence_btn.clicked.connect(
            lambda: asyncio.create_task(self.play_animation_sequence())
        )
        advanced_layout.addWidget(sequence_btn)

        layout.addWidget(advanced_group)

        # Status
        self.status_label = QLabel("Ready to animate!")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        layout.addWidget(self.status_label)

        layout.addStretch()
        return panel

    def create_display_panel(self) -> QWidget:
        """Create the pictograph display panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Title
        title = QLabel("🎨 Pictograph Animation Stage")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Display area for pictographs
        self.display_area = QWidget()
        self.display_area.setMinimumSize(800, 600)
        self.display_area.setStyleSheet(
            """
            QWidget {
                background-color: #f0f0f0;
                border: 2px solid #ccc;
                border-radius: 10px;
            }
        """
        )
        layout.addWidget(self.display_area)

        # Info panel
        info_label = QLabel(
            """
        <b>Demo Features:</b><br>
        • Real TKA pictograph rendering<br>
        • Smooth fade in/out animations<br>
        • Cross-fade transitions between pictographs<br>
        • Movement animations with easing<br>
        • Undo/redo support<br>
        • Configurable duration and easing<br>
        • Event-driven architecture<br>
        """
        )
        info_label.setStyleSheet(
            "background-color: #e8f4f8; padding: 10px; border-radius: 5px;"
        )
        layout.addWidget(info_label)

        return panel

    def create_sample_pictographs(self):
        """Create sample pictographs using real CSV data."""
        try:
            # Load CSV data
            csv_data = self.csv_manager._load_csv_data()
            if csv_data.empty:
                self.update_status("No CSV data available")
                return

            # Get first few entries for different letters
            sample_entries = []

            # Get some A pictographs
            a_entries = csv_data[csv_data["letter"] == "A"].head(2)
            sample_entries.extend(a_entries.to_dict("records"))

            # Get a B pictograph if available
            b_entries = csv_data[csv_data["letter"] == "B"].head(1)
            if not b_entries.empty:
                sample_entries.extend(b_entries.to_dict("records"))

            # If we don't have enough, just take first 3 entries
            if len(sample_entries) < 3:
                sample_entries = csv_data.head(3).to_dict("records")

            for i, entry in enumerate(sample_entries[:3]):  # Limit to 3 pictographs
                try:
                    # Create pictograph data using the factory
                    pictograph_data = (
                        self.pictograph_factory.create_pictograph_data_from_entry(
                            entry, "diamond"
                        )
                    )

                    # Create pictograph component using the factory function
                    from desktop.modern.presentation.components.pictograph.pictograph_widget import (
                        create_pictograph_widget,
                    )

                    pictograph = create_pictograph_widget(
                        parent=self.display_area, container=self.container
                    )

                    # Position the pictograph
                    pictograph.resize(300, 300)
                    pictograph.move(50 + i * 320, 50)

                    # Make it visible and show it
                    pictograph.setAttribute(
                        Qt.WidgetAttribute.WA_DontShowOnScreen, False
                    )
                    pictograph.setVisible(True)
                    pictograph.show()

                    # Render the pictograph
                    pictograph.update_from_pictograph_data(pictograph_data)

                    # Initially hide all but the first
                    if i > 0:
                        pictograph.setVisible(False)

                    self.pictographs.append(pictograph)

                    self.update_status(
                        f"Created pictograph {i + 1}: {entry.get('letter', '?')} - {entry.get('start_pos', '?')} to {entry.get('end_pos', '?')}"
                    )

                except Exception as e:
                    self.update_status(f"Error creating pictograph {i}: {e}")
                    print(f"Detailed error for pictograph {i}: {e}")
                    import traceback

                    traceback.print_exc()

            if self.pictographs:
                self.update_status(
                    f"Successfully created {len(self.pictographs)} real pictographs from CSV data!"
                )
            else:
                self.update_status("Failed to create any pictographs")

        except Exception as e:
            self.update_status(f"Error loading CSV data: {e}")
            print(f"Detailed error: {e}")
            import traceback

            traceback.print_exc()

    def update_status(self, message: str):
        """Update the status label."""
        self.status_label.setText(message)
        print(f"Status: {message}")

    def update_duration(self, value: float, label: QLabel):
        """Update animation duration."""
        self.animation_duration = value
        label.setText(f"Duration: {value:.1f}s")

    def update_easing(self, easing_name: str):
        """Update easing type."""
        easing_map = {
            "Linear": EasingType.LINEAR,
            "Ease In-Out": EasingType.EASE_IN_OUT,
            "Ease In": EasingType.EASE_IN,
            "Ease Out": EasingType.EASE_OUT,
            "Spring": EasingType.SPRING,
        }
        self.current_easing = easing_map.get(easing_name, EasingType.EASE_IN_OUT)

    def get_current_pictograph(self) -> PictographWidget | None:
        """Get the currently active pictograph."""
        if 0 <= self.current_pictograph_index < len(self.pictographs):
            return self.pictographs[self.current_pictograph_index]
        return None

    async def fade_current_pictograph(self, fade_in: bool):
        """Fade the current pictograph in or out."""
        pictograph = self.get_current_pictograph()
        if not pictograph:
            self.update_status("No pictograph to animate")
            return

        try:
            config = AnimationConfig(
                duration=self.animation_duration, easing=self.current_easing
            )

            action = "in" if fade_in else "out"
            self.update_status(f"Fading pictograph {action}...")

            animation_id = await self.animator.fade_target(pictograph, fade_in, config)

            self.update_status(f"Fade {action} complete! (ID: {animation_id[:8]})")

        except Exception as e:
            self.update_status(f"Animation failed: {e}")

    async def crossfade_to_next(self):
        """Cross-fade to the next pictograph."""
        if len(self.pictographs) < 2:
            self.update_status("Need at least 2 pictographs for cross-fade")
            return

        current = self.get_current_pictograph()
        next_index = (self.current_pictograph_index + 1) % len(self.pictographs)
        next_pictograph = self.pictographs[next_index]

        if not current:
            self.update_status("No current pictograph")
            return

        try:
            config = AnimationConfig(
                duration=self.animation_duration, easing=self.current_easing
            )

            self.update_status("Cross-fading to next pictograph...")

            # Make next pictograph visible but transparent
            next_pictograph.setVisible(True)

            # Cross-fade
            out_id, in_id = await self.animator.cross_fade_targets(
                current, next_pictograph, config
            )

            # Update current index
            self.current_pictograph_index = next_index

            self.update_status(
                f"Cross-fade complete! Out: {out_id[:8]}, In: {in_id[:8]}"
            )

        except Exception as e:
            self.update_status(f"Cross-fade failed: {e}")

    async def crossfade_to_previous(self):
        """Cross-fade to the previous pictograph."""
        if len(self.pictographs) < 2:
            self.update_status("Need at least 2 pictographs for cross-fade")
            return

        current = self.get_current_pictograph()
        prev_index = (self.current_pictograph_index - 1) % len(self.pictographs)
        prev_pictograph = self.pictographs[prev_index]

        if not current:
            self.update_status("No current pictograph")
            return

        try:
            config = AnimationConfig(
                duration=self.animation_duration, easing=self.current_easing
            )

            self.update_status("Cross-fading to previous pictograph...")

            # Make previous pictograph visible but transparent
            prev_pictograph.setVisible(True)

            # Cross-fade
            out_id, in_id = await self.animator.cross_fade_targets(
                current, prev_pictograph, config
            )

            # Update current index
            self.current_pictograph_index = prev_index

            self.update_status(
                f"Cross-fade complete! Out: {out_id[:8]}, In: {in_id[:8]}"
            )

        except Exception as e:
            self.update_status(f"Cross-fade failed: {e}")

    async def move_pictograph(self, dx: int, dy: int):
        """Move the current pictograph by the specified offset."""
        pictograph = self.get_current_pictograph()
        if not pictograph:
            self.update_status("No pictograph to move")
            return

        try:
            current_x = pictograph.x()
            current_y = pictograph.y()
            new_x = current_x + dx
            new_y = current_y + dy

            config = AnimationConfig(
                duration=self.animation_duration, easing=self.current_easing
            )

            self.update_status(f"Moving pictograph by ({dx}, {dy})...")

            # Animate X position
            x_id = await self.animator.animate_property(
                pictograph, "x", current_x, new_x, config
            )

            # Animate Y position simultaneously
            y_id = await self.animator.animate_property(
                pictograph, "y", current_y, new_y, config
            )

            self.update_status(f"Move complete! X: {x_id[:8]}, Y: {y_id[:8]}")

        except Exception as e:
            self.update_status(f"Move failed: {e}")

    async def center_pictograph(self):
        """Center the current pictograph in the display area."""
        pictograph = self.get_current_pictograph()
        if not pictograph:
            self.update_status("No pictograph to center")
            return

        try:
            # Calculate center position
            center_x = (self.display_area.width() - pictograph.width()) // 2
            center_y = (self.display_area.height() - pictograph.height()) // 2

            current_x = pictograph.x()
            current_y = pictograph.y()

            config = AnimationConfig(
                duration=self.animation_duration, easing=self.current_easing
            )

            self.update_status("Centering pictograph...")

            # Animate to center
            x_id = await self.animator.animate_property(
                pictograph, "x", current_x, center_x, config
            )
            y_id = await self.animator.animate_property(
                pictograph, "y", current_y, center_y, config
            )

            self.update_status(f"Centering complete! X: {x_id[:8]}, Y: {y_id[:8]}")

        except Exception as e:
            self.update_status(f"Centering failed: {e}")

    async def undo_animation(self):
        """Undo the last animation."""
        try:
            self.update_status("Undoing last animation...")

            success = await self.animator.undo_last_command()

            if success:
                self.update_status("Undo successful!")
            else:
                self.update_status("Nothing to undo")

        except Exception as e:
            self.update_status(f"Undo failed: {e}")

    async def play_animation_sequence(self):
        """Play a sequence of animations to showcase the system."""
        try:
            self.update_status("Playing animation sequence...")

            pictograph = self.get_current_pictograph()
            if not pictograph:
                self.update_status("No pictograph for sequence")
                return

            config = AnimationConfig(duration=0.8, easing=EasingType.SPRING)

            # Sequence: fade out, move, fade in, center
            await self.animator.fade_target(pictograph, False, config)
            await asyncio.sleep(0.2)

            await self.animator.animate_property(
                pictograph, "x", pictograph.x(), pictograph.x() + 100, config
            )
            await asyncio.sleep(0.2)

            await self.animator.fade_target(pictograph, True, config)
            await asyncio.sleep(0.5)

            # Center it
            center_x = (self.display_area.width() - pictograph.width()) // 2
            await self.animator.animate_property(
                pictograph, "x", pictograph.x(), center_x, config
            )

            self.update_status("Animation sequence complete!")

        except Exception as e:
            self.update_status(f"Sequence failed: {e}")


def main():
    """Run the interactive animation demo."""
    app = QApplication(sys.argv)

    # Set up event loop for async operations
    try:
        import qasync

        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)

        demo = InteractiveAnimationDemo()
        demo.show()

        print("🎭 Interactive Animation Demo Started!")
        print("Use the controls to test the animation system with real pictographs.")

        with loop:
            loop.run_forever()

    except ImportError:
        print("qasync not available, running without async support")
        print("Install qasync: pip install qasync")

        demo = InteractiveAnimationDemo()
        demo.show()

        app.exec()


if __name__ == "__main__":
    main()
