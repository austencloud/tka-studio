"""
ConstructTabLayoutManager

Handles UI layout setup, panel creation, and widget management for the construct tab.
Responsible for creating the main layout structure and organizing UI components.
"""

from typing import Optional, Callable
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QStackedWidget,
)
from PyQt6.QtCore import Qt

from core.dependency_injection.di_container import DIContainer
from presentation.factories.workbench_factory import (
    create_modern_workbench,
)
from presentation.components.option_picker.option_picker import (
    OptionPicker,
)


class ConstructTabLayoutManager:
    """
    Manages the UI layout and panel creation for the construct tab.

    Responsibilities:
    - Setting up the main horizontal layout (50/50 split)
    - Creating workbench panel (left side)
    - Creating picker panel with stacked widget (right side)
    - Managing progress callbacks during initialization
    """

    def __init__(
        self,
        container: DIContainer,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ):
        self.container = container
        self.progress_callback = progress_callback

        # UI components that will be created
        self.workbench = None
        self.picker_stack = None
        self.start_position_picker = None
        self.option_picker = None

    def setup_ui(self, parent_widget: QWidget) -> None:
        """Setup the main UI layout with progress updates"""
        if self.progress_callback:
            self.progress_callback("Setting up construct tab layout...", 0.1)

        # Main horizontal layout: 50/50 split like Legacy
        main_layout = QHBoxLayout(parent_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(12, 12, 12, 12)

        if self.progress_callback:
            self.progress_callback("Creating sequence workbench panel...", 0.2)

        # Left panel: Sequence Workbench (50% width)
        workbench_panel = self._create_workbench_panel()
        main_layout.addWidget(workbench_panel, 1)  # Equal weight = 50%

        if self.progress_callback:
            self.progress_callback("Creating option picker panel...", 0.5)

        # Right panel: Option Picker (50% width)
        picker_panel = self._create_picker_panel_with_progress()
        main_layout.addWidget(picker_panel, 1)  # Equal weight = 50%

        # CRITICAL: Connect beat frame to graph editor after both components are created
        self._connect_beat_frame_to_graph_editor()

        if self.progress_callback:
            self.progress_callback("Construct tab layout complete!", 1.0)

    def _create_workbench_panel(self) -> QWidget:
        """Create the left panel containing sequence workbench"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Create modern workbench with integrated button panel
        self.workbench = create_modern_workbench(self.container, panel)
        layout.addWidget(self.workbench)

        return panel

    def _create_picker_panel_with_progress(self) -> QWidget:
        """Create the right panel containing start pos picker and option picker"""
        if self.progress_callback:
            self.progress_callback("Creating picker panel layout...", 0.6)

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Create stacked widget for picker views (like Legacy)
        self.picker_stack = QStackedWidget()

        if self.progress_callback:
            self.progress_callback("Initializing start position picker...", 0.7)

        # Index 0: Start Position Picker
        start_pos_widget = self._create_start_position_widget()
        self.picker_stack.addWidget(start_pos_widget)

        if self.progress_callback:
            self.progress_callback("Loading option picker dataset...", 0.8)

        # Index 1: Option Picker
        option_widget = self._create_option_picker_widget_with_progress()
        self.picker_stack.addWidget(option_widget)

        if self.progress_callback:
            self.progress_callback("Creating graph editor widget...", 0.85)

        # Index 2: Graph Editor
        graph_editor_widget = self._create_graph_editor_widget()
        self.picker_stack.addWidget(graph_editor_widget)

        if self.progress_callback:
            self.progress_callback("Configuring picker transitions...", 0.9)

        # Start with start position picker visible
        self.picker_stack.setCurrentIndex(0)

        layout.addWidget(self.picker_stack)
        return panel

    def _create_start_position_widget(self) -> QWidget:
        """Create start position picker widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        from ...components.start_position_picker.start_position_picker import (
            StartPositionPicker,
        )

        self.start_position_picker = StartPositionPicker()
        layout.addWidget(self.start_position_picker)

        return widget

    def _create_option_picker_widget_with_progress(self) -> QWidget:
        """Create option picker widget with progress updates for the heavy initialization"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        try:
            # Create progress callback for ModernOptionPicker's internal initialization
            def option_picker_progress(step: str, progress: float):
                if self.progress_callback:
                    # Map option picker progress (0.0-1.0) to our remaining range
                    mapped_progress = 0.8 + (progress * 0.1)  # 0.8 to 0.9 range
                    self.progress_callback(f"Option picker: {step}", mapped_progress)

            self.option_picker = OptionPicker(
                self.container, progress_callback=option_picker_progress
            )
            self.option_picker.initialize()
            layout.addWidget(self.option_picker.widget)
        except RuntimeError as e:
            print(f"❌ Failed to create option picker: {e}")
            # Create fallback widget
            fallback_label = QLabel("Option picker unavailable")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)
            self.option_picker = None

        return widget

    def _create_graph_editor_widget(self) -> QWidget:
        """Create graph editor widget for embedded use in stack widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        try:
            # Import simplified graph editor
            from ...components.workbench.graph_editor.graph_editor import GraphEditor

            # Create graph editor without complex dependencies (embedded mode)
            self.graph_editor = GraphEditor(
                graph_service=None,  # Simplified version doesn't require service
                parent=None,  # No parent workbench for embedded mode
                workbench_width=800,  # Default width, will be resized by container
                workbench_height=300,  # Fixed height for embedded mode
            )

            layout.addWidget(self.graph_editor)

            # Connect graph editor signals if needed
            if hasattr(self.graph_editor, "beat_modified"):
                self.graph_editor.beat_modified.connect(self._on_graph_beat_modified)

        except Exception as e:
            # Fallback if graph editor creation fails
            fallback_label = QLabel(f"Graph editor unavailable: {e}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet("color: red; font-size: 14px; padding: 20px;")
            layout.addWidget(fallback_label)
            self.graph_editor = None

            # Log the error for debugging
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create graph editor: {e}", exc_info=True)

        return widget

    def _on_graph_beat_modified(self, beat_index: int, beat_data):
        """Handle beat modification from graph editor"""
        # Forward to sequence manager or other components as needed
        print(f"🎵 Graph editor: Beat {beat_index} modified: {beat_data}")
        # TODO: Connect to sequence manager when available

    def transition_to_option_picker(self):
        """Switch from start position picker to option picker"""
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(1)

    def transition_to_start_position_picker(self):
        """Switch back to start position picker"""
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(0)

    def transition_to_graph_editor(self):
        """Switch to graph editor"""
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(2)

    def _connect_beat_frame_to_graph_editor(self):
        """Connect beat frame selection signals to graph editor"""
        if not self.workbench or not self.graph_editor:
            return

        # Get the beat frame from the workbench
        beat_frame_section = getattr(self.workbench, "_beat_frame_section", None)
        if not beat_frame_section:
            return

        beat_frame = getattr(beat_frame_section, "_beat_frame", None)
        if not beat_frame:
            return

        # Connect beat selection signal to graph editor
        beat_frame.beat_selected.connect(self._on_beat_selected_for_graph_editor)

        print("✅ Connected beat frame to graph editor")

    def _on_beat_selected_for_graph_editor(self, beat_index: int):
        """Handle beat selection from beat frame and update graph editor"""
        print(f"🔍 DEBUG: Beat selection received - index: {beat_index}")

        if not self.graph_editor or not self.workbench:
            print(
                f"⚠️ Missing components - graph_editor: {bool(self.graph_editor)}, workbench: {bool(self.workbench)}"
            )
            return

        # Get current sequence from workbench
        current_sequence = self.workbench.get_sequence()
        if not current_sequence:
            print(f"⚠️ No current sequence available")
            return

        print(f"🔍 DEBUG: Current sequence has {len(current_sequence.beats)} beats")

        # Handle start position selection (index -1)
        if beat_index == -1:
            # Get start position data from workbench
            start_position_data = getattr(self.workbench, "_start_position_data", None)
            if start_position_data:
                self.graph_editor.set_selected_beat_data(-1, start_position_data)
                print(f"✅ Graph editor updated with start position")
            else:
                print(f"⚠️ No start position data available")
            return

        # Handle regular beat selection
        if 0 <= beat_index < len(current_sequence.beats):
            beat_data = current_sequence.beats[beat_index]
            print(
                f"🔍 DEBUG: Beat data - letter: {beat_data.letter}, beat_number: {beat_data.beat_number}"
            )
            self.graph_editor.set_selected_beat_data(beat_index, beat_data)
            print(f"✅ Graph editor updated with beat {beat_index + 1}")
        else:
            print(
                f"⚠️ Invalid beat index: {beat_index} (sequence has {len(current_sequence.beats)} beats)"
            )

    def _on_graph_beat_modified(self, beat_index: int, beat_data):
        """Handle beat modification from graph editor"""
        print(f"✅ Graph editor modified beat {beat_index}")
        # TODO: Implement beat modification handling
