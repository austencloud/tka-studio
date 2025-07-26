"""
Comprehensive Standalone Sequence Workbench

A polished, integrated testing environment that combines:
- Sequence Beat Frame with AABB sequence
- Graph Editor with proper pictograph scaling
- Animation System with sequence playback
- Interactive Selection with real-time updates

This serves as both a testing environment and a reference implementation
for component integration patterns in TKA.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from desktop.modern.presentation.components.graph_editor.components.adjustment_panel import (
    AdjustmentPanel,
)
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

# Add modern/src to path for imports
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

from desktop.modern.domain.models.beat_models import BeatData
from desktop.modern.domain.models.enums import Location, MotionType, Orientation, RotationDirection
from desktop.modern.domain.models.motion_models import MotionData
from desktop.modern.domain.models.sequence_data import SequenceData
from desktop.modern.presentation.components.pictograph.pictograph_widget import (
    create_pictograph_widget,
)


# Component Integration Framework
class WorkbenchEventBus:
    """Unified event bus for component communication"""

    def __init__(self):
        self._subscribers: Dict[str, List[callable]] = {}

    def subscribe(self, event_type: str, callback: callable):
        """Subscribe to an event type"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def emit(self, event_type: str, data: Any = None):
        """Emit an event to all subscribers"""
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"❌ Event callback error: {e}")


class SequenceAnimationEngine:
    """Animation engine for sequence playback"""

    def __init__(self, event_bus: WorkbenchEventBus):
        self.event_bus = event_bus
        self.sequence: Optional[SequenceData] = None
        self.current_beat_index = -1  # -1 = start position
        self.is_playing = False
        self.playback_speed = 1.0  # 1.0 = normal speed

        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._advance_beat)

        # Animation settings
        self.beat_duration = 1000  # ms per beat

        # Visual feedback for animation
        self.animation_callbacks = []

    def set_sequence(self, sequence: SequenceData):
        """Set the sequence for animation"""
        self.sequence = sequence
        self.current_beat_index = -1
        self.stop()

    def play(self):
        """Start sequence playback"""
        if not self.sequence:
            return

        self.is_playing = True
        interval = int(self.beat_duration / self.playback_speed)
        self.timer.start(interval)
        self.event_bus.emit("animation.started")

    def pause(self):
        """Pause sequence playback"""
        self.is_playing = False
        self.timer.stop()
        self.event_bus.emit("animation.paused")

    def stop(self):
        """Stop sequence playback and reset"""
        self.is_playing = False
        self.timer.stop()
        self.current_beat_index = -1
        self.event_bus.emit("animation.stopped")
        self.event_bus.emit("beat.selected", -1)  # Select start position

    def set_speed(self, speed: float):
        """Set playback speed (0.5 = half speed, 2.0 = double speed)"""
        self.playback_speed = max(0.1, min(3.0, speed))
        if self.is_playing:
            # Restart timer with new interval
            interval = int(self.beat_duration / self.playback_speed)
            self.timer.start(interval)

    def seek_to_beat(self, beat_index: int):
        """Seek to specific beat"""
        if not self.sequence:
            return

        max_index = len(self.sequence.beats) - 1
        self.current_beat_index = max(-1, min(beat_index, max_index))
        self.event_bus.emit("beat.selected", self.current_beat_index)

    def _advance_beat(self):
        """Advance to next beat in sequence"""
        if not self.sequence:
            return

        self.current_beat_index += 1

        # Check if we've reached the end
        if self.current_beat_index >= len(self.sequence.beats):
            self.stop()
            return

        # Emit beat selection event with animation context
        self.event_bus.emit("beat.selected", self.current_beat_index)
        self.event_bus.emit(
            "animation.beat_changed",
            {
                "beat_index": self.current_beat_index,
                "total_beats": len(self.sequence.beats),
                "progress": (self.current_beat_index + 1) / len(self.sequence.beats),
            },
        )


class MockLayoutService:
    """Mock layout service for standalone operation"""

    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: tuple
    ) -> Dict[str, int]:
        """Calculate optimal layout for beat frame"""
        if not sequence or len(sequence.beats) == 0:
            return {"rows": 1, "columns": 1}

        beat_count = len(sequence.beats) + 1  # +1 for start position

        # Simple layout calculation
        if beat_count <= 4:
            return {"rows": 1, "columns": beat_count}
        elif beat_count <= 8:
            return {"rows": 2, "columns": 4}
        else:
            columns = min(8, int((beat_count**0.5) + 1))
            rows = (beat_count + columns - 1) // columns
            return {"rows": rows, "columns": columns}


class MockGraphEditorService:
    """Mock graph editor service for standalone operation"""

    def __init__(self):
        self.current_beat: Optional[BeatData] = None

    def set_beat_data(self, beat_data: BeatData):
        """Set current beat data"""
        self.current_beat = beat_data

    def get_beat_data(self) -> Optional[BeatData]:
        """Get current beat data"""
        return self.current_beat


class SimpleBeatFrameWidget(QWidget):
    """Simplified beat frame for standalone workbench"""

    beat_selected = pyqtSignal(int)

    def __init__(self, event_bus: WorkbenchEventBus):
        super().__init__()
        self.event_bus = event_bus
        self.sequence: Optional[SequenceData] = None
        self.start_position: Optional[BeatData] = None
        self.selected_beat_index: Optional[int] = None
        self.beat_buttons: List[QPushButton] = []

        self._setup_ui()
        self._connect_events()

    def _setup_ui(self):
        """Setup the beat frame UI"""
        self.layout = QGridLayout(self)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("Sequence Beat Frame")
        title.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title, 0, 0, 1, 4)

    def _connect_events(self):
        """Connect to event bus"""
        self.event_bus.subscribe("beat.selected", self._on_beat_selected_externally)

    def set_sequence(self, sequence: SequenceData, start_position: BeatData):
        """Set sequence and start position data"""
        self.sequence = sequence
        self.start_position = start_position
        self._rebuild_beat_grid()

    def _rebuild_beat_grid(self):
        """Rebuild the beat grid layout"""
        # Clear existing buttons
        for button in self.beat_buttons:
            button.deleteLater()
        self.beat_buttons.clear()

        if not self.sequence:
            return

        # Create start position button
        start_btn = QPushButton("α\nStart")
        start_btn.setFixedSize(80, 60)
        start_btn.clicked.connect(lambda: self._select_beat(-1))
        start_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2E3440;
                border: 2px solid #4C566A;
                border-radius: 8px;
                color: #ECEFF4;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3B4252;
                border-color: #5E81AC;
            }
            QPushButton:pressed {
                background-color: #434C5E;
            }
        """
        )
        self.layout.addWidget(start_btn, 1, 0)
        self.beat_buttons.append(start_btn)

        # Create beat buttons
        for i, beat in enumerate(self.sequence.beats):
            btn = QPushButton(f"{beat.letter}\nBeat {i+1}")
            btn.setFixedSize(80, 60)
            btn.clicked.connect(lambda checked, idx=i: self._select_beat(idx))
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #2E3440;
                    border: 2px solid #4C566A;
                    border-radius: 8px;
                    color: #ECEFF4;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3B4252;
                    border-color: #5E81AC;
                }
                QPushButton:pressed {
                    background-color: #434C5E;
                }
            """
            )

            # Calculate grid position
            col = (i + 1) % 4
            row = 1 + (i + 1) // 4
            self.layout.addWidget(btn, row, col)
            self.beat_buttons.append(btn)

    def _select_beat(self, beat_index: int):
        """Select a beat and emit signal"""
        self.selected_beat_index = beat_index
        self._update_selection_visual()
        self.beat_selected.emit(beat_index)
        self.event_bus.emit("beat.selected", beat_index)

    def _on_beat_selected_externally(self, beat_index: int):
        """Handle beat selection from external source (e.g., animation)"""
        self.selected_beat_index = beat_index
        self._update_selection_visual()

    def _update_selection_visual(self):
        """Update visual selection indicators"""
        for i, button in enumerate(self.beat_buttons):
            if i == 0 and self.selected_beat_index == -1:
                # Start position selected
                button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #5E81AC;
                        border: 2px solid #88C0D0;
                        border-radius: 8px;
                        color: #ECEFF4;
                        font-weight: bold;
                    }
                """
                )
            elif i > 0 and self.selected_beat_index == i - 1:
                # Regular beat selected
                button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #5E81AC;
                        border: 2px solid #88C0D0;
                        border-radius: 8px;
                        color: #ECEFF4;
                        font-weight: bold;
                    }
                """
                )
            else:
                # Not selected
                button.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #2E3440;
                        border: 2px solid #4C566A;
                        border-radius: 8px;
                        color: #ECEFF4;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #3B4252;
                        border-color: #5E81AC;
                    }
                    QPushButton:pressed {
                        background-color: #434C5E;
                    }
                """
                )


class ComprehensiveSequenceWorkbench(QMainWindow):
    """Comprehensive standalone sequence workbench"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TKA Comprehensive Sequence Workbench")
        self.setGeometry(100, 100, 1600, 1000)

        # Initialize systems
        self.event_bus = WorkbenchEventBus()
        self.animation_engine = SequenceAnimationEngine(self.event_bus)

        # Mock services
        self.layout_service = MockLayoutService()
        self.graph_service = MockGraphEditorService()

        # Create test data
        self.sequence_data = self._create_aabb_sequence()
        self.start_position_data = self._create_start_position()

        # Setup UI
        self._setup_ui()
        self._connect_signals()
        self._load_test_data()

        print("🎉 Comprehensive Sequence Workbench initialized")
        print(
            f"📊 Loaded sequence: {self.sequence_data.name} with {len(self.sequence_data.beats)} beats"
        )

    def _setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Title
        title = QLabel("TKA Comprehensive Sequence Workbench")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2E3440; margin: 10px;")
        main_layout.addWidget(title)

        # Create main content splitter
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(content_splitter)

        # Left panel: Beat frame and controls
        left_panel = self._create_left_panel()
        content_splitter.addWidget(left_panel)

        # Right panel: Graph editor and animation
        right_panel = self._create_right_panel()
        content_splitter.addWidget(right_panel)

        # Set splitter proportions (40% left, 60% right)
        content_splitter.setSizes([640, 960])

        # Bottom status bar
        self._create_status_bar()

    def _create_left_panel(self) -> QWidget:
        """Create the left panel with beat frame and controls"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        # Beat frame
        self.beat_frame = SimpleBeatFrameWidget(self.event_bus)
        layout.addWidget(self.beat_frame)

        # Animation controls
        controls_group = QGroupBox("Animation Controls")
        controls_layout = QVBoxLayout(controls_group)

        # Playback buttons
        button_layout = QHBoxLayout()

        self.play_btn = QPushButton("▶ Play")
        self.play_btn.clicked.connect(self._toggle_playback)
        button_layout.addWidget(self.play_btn)

        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.clicked.connect(self.animation_engine.stop)
        button_layout.addWidget(self.stop_btn)

        controls_layout.addLayout(button_layout)

        # Speed control
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Speed:"))

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(10, 300)  # 0.1x to 3.0x speed
        self.speed_slider.setValue(100)  # 1.0x speed
        self.speed_slider.valueChanged.connect(self._on_speed_changed)
        speed_layout.addWidget(self.speed_slider)

        self.speed_label = QLabel("1.0x")
        speed_layout.addWidget(self.speed_label)

        controls_layout.addLayout(speed_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        controls_layout.addWidget(self.progress_bar)

        layout.addWidget(controls_group)

        # Add stretch to push everything to top
        layout.addStretch()

        return panel

    def _create_right_panel(self) -> QWidget:
        """Create the right panel with graph editor and visualization"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        # Graph editor section
        graph_group = QGroupBox("Graph Editor & Pictograph Display")
        graph_layout = QVBoxLayout(graph_group)

        # Current beat info
        self.beat_info_label = QLabel("No beat selected")
        self.beat_info_label.setFont(QFont("Inter", 11, QFont.Weight.Bold))
        self.beat_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.beat_info_label.setStyleSheet(
            """
            QLabel {
                background-color: #ECEFF4;
                border: 1px solid #D8DEE9;
                border-radius: 6px;
                padding: 8px;
                color: #2E3440;
            }
        """
        )
        graph_layout.addWidget(self.beat_info_label)

        # Real pictograph display using TKA components
        pictograph_container = QWidget()
        pictograph_container.setMinimumSize(400, 400)
        pictograph_container.setStyleSheet(
            """
            QWidget {
                background-color: #F8F9FA;
                border: 2px solid #D8DEE9;
                border-radius: 12px;
            }
        """
        )

        pictograph_layout = QVBoxLayout(pictograph_container)
        pictograph_layout.setContentsMargins(10, 10, 10, 10)

        # Create actual pictograph component
        self.pictograph_component = create_pictograph_widget()
        self.pictograph_component.setMinimumSize(380, 300)
        pictograph_layout.addWidget(self.pictograph_component)

        # Add adjustment panels for testing
        panels_layout = QHBoxLayout()

        # Blue (left) adjustment panel
        self.blue_adjustment_panel = AdjustmentPanel(self, side="left")
        self.blue_adjustment_panel.setMaximumHeight(80)
        panels_layout.addWidget(QLabel("Blue Controls:"))
        panels_layout.addWidget(self.blue_adjustment_panel)

        # Red (right) adjustment panel
        self.red_adjustment_panel = AdjustmentPanel(self, side="right")
        self.red_adjustment_panel.setMaximumHeight(80)
        panels_layout.addWidget(QLabel("Red Controls:"))
        panels_layout.addWidget(self.red_adjustment_panel)

        pictograph_layout.addLayout(panels_layout)
        graph_layout.addWidget(pictograph_container)

        # Beat data details
        details_group = QGroupBox("Beat Data Details")
        details_layout = QGridLayout(details_group)

        # Motion data display
        self.blue_motion_label = QLabel("Blue Motion: -")
        self.red_motion_label = QLabel("Red Motion: -")
        self.timing_label = QLabel("Timing: -")
        self.duration_label = QLabel("Duration: -")

        details_layout.addWidget(QLabel("Blue Motion:"), 0, 0)
        details_layout.addWidget(self.blue_motion_label, 0, 1)
        details_layout.addWidget(QLabel("Red Motion:"), 1, 0)
        details_layout.addWidget(self.red_motion_label, 1, 1)
        details_layout.addWidget(QLabel("Timing:"), 2, 0)
        details_layout.addWidget(self.timing_label, 2, 1)
        details_layout.addWidget(QLabel("Duration:"), 3, 0)
        details_layout.addWidget(self.duration_label, 3, 1)

        graph_layout.addWidget(details_group)
        layout.addWidget(graph_group)

        # Visualization controls
        viz_group = QGroupBox("Visualization Controls")
        viz_layout = QVBoxLayout(viz_group)

        # Test buttons for different scenarios
        test_layout = QGridLayout()

        test_start_btn = QPushButton("Test Start Position")
        test_start_btn.clicked.connect(lambda: self._test_beat_selection(-1))
        test_layout.addWidget(test_start_btn, 0, 0)

        test_beat1_btn = QPushButton("Test Beat 1 (A)")
        test_beat1_btn.clicked.connect(lambda: self._test_beat_selection(0))
        test_layout.addWidget(test_beat1_btn, 0, 1)

        test_beat2_btn = QPushButton("Test Beat 2 (A)")
        test_beat2_btn.clicked.connect(lambda: self._test_beat_selection(1))
        test_layout.addWidget(test_beat2_btn, 1, 0)

        test_beat3_btn = QPushButton("Test Beat 3 (B)")
        test_beat3_btn.clicked.connect(lambda: self._test_beat_selection(2))
        test_layout.addWidget(test_beat3_btn, 1, 1)

        viz_layout.addLayout(test_layout)
        layout.addWidget(viz_group)

        return panel

    def _create_status_bar(self):
        """Create status bar with system information"""
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_layout.setContentsMargins(10, 5, 10, 5)

        self.status_label = QLabel(
            "Ready - Click beats to test selection and visualization"
        )
        self.status_label.setStyleSheet("color: #5E81AC; font-weight: bold;")
        status_layout.addWidget(self.status_label)

        status_layout.addStretch()

        # System info
        info_label = QLabel("TKA Modern Architecture | PyQt6 | Clean Architecture")
        info_label.setStyleSheet("color: #4C566A; font-size: 10px;")
        status_layout.addWidget(info_label)

        # Add status widget to main window
        self.setCentralWidget(self.centralWidget())
        main_layout = self.centralWidget().layout()
        main_layout.addWidget(status_widget)

    def _connect_signals(self):
        """Connect component signals and event bus"""
        # Beat frame signals
        self.beat_frame.beat_selected.connect(self._on_beat_selected)

        # Event bus subscriptions
        self.event_bus.subscribe("beat.selected", self._on_beat_selected_via_event)
        self.event_bus.subscribe("animation.started", self._on_animation_started)
        self.event_bus.subscribe("animation.paused", self._on_animation_paused)
        self.event_bus.subscribe("animation.stopped", self._on_animation_stopped)

    def _load_test_data(self):
        """Load test sequence data into components"""
        # Set sequence in animation engine
        self.animation_engine.set_sequence(self.sequence_data)

        # Set sequence in beat frame
        self.beat_frame.set_sequence(self.sequence_data, self.start_position_data)

        # Update progress bar range
        self.progress_bar.setRange(-1, len(self.sequence_data.beats) - 1)

        print("✅ Test data loaded successfully")

    def _create_aabb_sequence(self) -> SequenceData:
        """Create the AABB sequence from the provided JSON data"""
        beats = []

        # Beat 1: A (alpha1 -> alpha3)
        beat1 = BeatData(
            beat_number=1,
            letter="A",
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
        )

        # Beat 2: A (alpha3 -> alpha5)
        beat2 = BeatData(
            beat_number=2,
            letter="A",
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.WEST,
                end_loc=Location.NORTH,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.EAST,
                end_loc=Location.SOUTH,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
        )

        # Beat 3: B (alpha5 -> alpha3)
        beat3 = BeatData(
            beat_number=3,
            letter="B",
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.WEST,
                start_ori=Orientation.IN,
                end_ori=Orientation.OUT,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.EAST,
                start_ori=Orientation.IN,
                end_ori=Orientation.OUT,
                turns=0.0,
            ),
        )

        # Beat 4: B (alpha3 -> alpha1)
        beat4 = BeatData(
            beat_number=4,
            letter="B",
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.WEST,
                end_loc=Location.SOUTH,
                start_ori=Orientation.OUT,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.EAST,
                end_loc=Location.NORTH,
                start_ori=Orientation.OUT,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
        )

        beats = [beat1, beat2, beat3, beat4]

        return SequenceData(
            name="AABB",
            beats=beats,
            metadata={"word": "AABB", "level": 0, "prop_type": "staff"},
        )

    def _create_start_position(self) -> BeatData:
        """Create start position data for testing"""
        return BeatData(
            beat_number=1,  # Use 1 but mark as start position in metadata
            letter="α",
            duration=1.0,
            blue_motion=MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.SOUTH,
                end_loc=Location.SOUTH,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
            red_motion=MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.NO_ROTATION,
                start_loc=Location.NORTH,
                end_loc=Location.NORTH,
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
                turns=0.0,
            ),
            metadata={"is_start_position": True, "sequence_start_position": "alpha"},
        )

    # Event Handlers
    def _on_beat_selected(self, beat_index: int):
        """Handle beat selection from beat frame"""
        self._update_beat_display(beat_index)

    def _on_beat_selected_via_event(self, beat_index: int):
        """Handle beat selection via event bus (e.g., from animation)"""
        self._update_beat_display(beat_index)
        self._update_progress_bar(beat_index)

    def _update_beat_display(self, beat_index: int):
        """Update the display with selected beat information"""
        if beat_index == -1:
            # Start position selected
            beat_data = self.start_position_data
            self.beat_info_label.setText("Selected: Start Position (α)")
            self.status_label.setText(
                "Start position selected - shows orientation controls"
            )

            # Update pictograph component with start position
            self.pictograph_component.update_from_beat(beat_data)

            # Update adjustment panels with start position
            self.blue_adjustment_panel.set_beat(beat_data)
            self.red_adjustment_panel.set_beat(beat_data)

            # Update motion details
            self.blue_motion_label.setText("STATIC (S→S)")
            self.red_motion_label.setText("STATIC (N→N)")
            self.timing_label.setText("N/A (Start Position)")
            self.duration_label.setText("N/A (Start Position)")

        elif 0 <= beat_index < len(self.sequence_data.beats):
            # Regular beat selected
            beat_data = self.sequence_data.beats[beat_index]
            self.beat_info_label.setText(
                f"Selected: Beat {beat_index + 1} ({beat_data.letter})"
            )
            self.status_label.setText(
                f"Beat {beat_index + 1} selected - shows turns controls"
            )

            # Update pictograph component with beat data
            self.pictograph_component.update_from_beat(beat_data)

            # Update adjustment panels with beat data
            self.blue_adjustment_panel.set_beat(beat_data)
            self.red_adjustment_panel.set_beat(beat_data)

            # Update motion details
            blue_motion = beat_data.blue_motion
            red_motion = beat_data.red_motion

            self.blue_motion_label.setText(
                f"{blue_motion.motion_type.value} ({blue_motion.start_loc.value}→{blue_motion.end_loc.value})"
            )
            self.red_motion_label.setText(
                f"{red_motion.motion_type.value} ({red_motion.start_loc.value}→{red_motion.end_loc.value})"
            )
            self.timing_label.setText("Split")  # AABB sequence uses split timing
            self.duration_label.setText(f"{beat_data.duration} beat(s)")

        else:
            # Invalid selection
            self.beat_info_label.setText("Invalid Selection")
            self.status_label.setText("Invalid beat selection")

            # Clear pictograph
            self.pictograph_component.clear_pictograph()

            # Clear adjustment panels
            self.blue_adjustment_panel.set_beat(None)
            self.red_adjustment_panel.set_beat(None)

            # Clear motion details
            self.blue_motion_label.setText("-")
            self.red_motion_label.setText("-")
            self.timing_label.setText("-")
            self.duration_label.setText("-")

        print(f"🎯 Beat {beat_index} selected and display updated")
        print(
            f"📊 Pictograph updated with {'start position' if beat_index == -1 else f'beat {beat_index + 1}'} data"
        )
        print(f"🎛️ Adjustment panels updated with beat data")

    def _update_progress_bar(self, beat_index: int):
        """Update animation progress bar"""
        self.progress_bar.setValue(beat_index)

        # Calculate percentage
        total_beats = len(self.sequence_data.beats)
        if total_beats > 0:
            if beat_index == -1:
                percentage = 0
            else:
                percentage = int(((beat_index + 1) / total_beats) * 100)
            self.progress_bar.setFormat(
                f"Beat {beat_index + 1 if beat_index >= 0 else 'Start'} ({percentage}%)"
            )

    def _test_beat_selection(self, beat_index: int):
        """Test beat selection programmatically"""
        print(f"\n🧪 Testing beat selection: {beat_index}")
        self.event_bus.emit("beat.selected", beat_index)

    def _toggle_playback(self):
        """Toggle between play and pause"""
        if self.animation_engine.is_playing:
            self.animation_engine.pause()
        else:
            self.animation_engine.play()

    def _on_speed_changed(self, value: int):
        """Handle speed slider changes"""
        speed = value / 100.0  # Convert to 0.1x - 3.0x range
        self.animation_engine.set_speed(speed)
        self.speed_label.setText(f"{speed:.1f}x")

    def _on_animation_started(self, data=None):
        """Handle animation start"""
        self.play_btn.setText("⏸ Pause")
        self.status_label.setText("Animation playing - sequence in motion")

    def _on_animation_paused(self, data=None):
        """Handle animation pause"""
        self.play_btn.setText("▶ Play")
        self.status_label.setText("Animation paused - click play to continue")

    def _on_animation_stopped(self, data=None):
        """Handle animation stop"""
        self.play_btn.setText("▶ Play")
        self.status_label.setText("Animation stopped - back to start position")
        self.progress_bar.setValue(-1)
        self.progress_bar.setFormat("Start Position (0%)")


def main():
    """Main entry point for comprehensive workbench"""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Create and show workbench
    workbench = ComprehensiveSequenceWorkbench()
    workbench.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
