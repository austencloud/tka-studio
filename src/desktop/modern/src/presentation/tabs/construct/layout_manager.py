"""
ConstructTabLayoutManager

Handles UI layout setup, panel creation, and widget management for the construct tab.
Responsible for creating the main layout structure and organizing UI components.
"""

from typing import TYPE_CHECKING, Callable, Optional

from core.dependency_injection.di_container import DIContainer
from presentation.components.option_picker.components.option_picker import OptionPicker
from presentation.components.start_position_picker.start_position_picker import (
    PickerMode,
    StartPositionPicker,
)
from presentation.factories.workbench_factory import create_modern_workbench
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QStackedWidget, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from presentation.components.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
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
        self.workbench = None
        self.picker_stack = None
        self.start_position_picker = None
        self.option_picker = None

    def setup_ui(self, parent_widget: QWidget) -> None:
        if self.progress_callback:
            self.progress_callback("Setting up construct tab layout...", 0.1)

        main_layout = QHBoxLayout(parent_widget)
        main_layout.setSpacing(8)  # Reduced spacing for more width
        main_layout.setContentsMargins(4, 4, 4, 4)  # Minimal margins for more width

        if self.progress_callback:
            self.progress_callback("Creating sequence workbench panel...", 0.2)

        workbench_panel = self._create_workbench_panel()
        main_layout.addWidget(workbench_panel, 1)

        if self.progress_callback:
            self.progress_callback("Creating option picker panel...", 0.5)

        picker_panel = self._create_picker_panel_with_progress()
        main_layout.addWidget(picker_panel, 1)

        self._connect_beat_frame_to_graph_editor()

        if self.progress_callback:
            self.progress_callback("Construct tab layout complete!", 1.0)

    def _create_workbench_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(2, 2, 2, 2)  # Minimal margins for more space
        layout.setSpacing(4)  # Reduced spacing
        self.workbench = create_modern_workbench(self.container, panel)
        layout.addWidget(self.workbench.get_widget())
        return panel

    def _create_picker_panel_with_progress(self) -> QWidget:
        if self.progress_callback:
            self.progress_callback("Creating picker panel layout...", 0.6)

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)  # No margins for maximum width
        layout.setSpacing(4)  # Reduced spacing

        self.picker_stack = QStackedWidget()

        if self.progress_callback:
            self.progress_callback("Initializing start position picker...", 0.7)

        start_pos_widget = self._create_start_position_widget()
        self.picker_stack.addWidget(start_pos_widget)

        if self.progress_callback:
            self.progress_callback("Loading option picker dataset...", 0.8)

        option_widget = self._create_option_picker_widget_with_progress()
        self.picker_stack.addWidget(option_widget)

        if self.progress_callback:
            self.progress_callback("Creating graph editor widget...", 0.85)

        graph_editor_widget = self._create_graph_editor_widget()
        self.picker_stack.addWidget(graph_editor_widget)

        if self.progress_callback:
            self.progress_callback("Configuring picker transitions...", 0.9)

        self.picker_stack.setCurrentIndex(0)
        layout.addWidget(self.picker_stack)
        return panel

    def _create_start_position_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Get only the 4 services we actually need
        from application.services.pictograph_pool_manager import PictographPoolManager
        from core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionUIService,
        )

        # Resolve the 4 required services from DI container
        pool_manager = self.container.resolve(PictographPoolManager)
        data_service = self.container.resolve(IStartPositionDataService)
        ui_service = self.container.resolve(IStartPositionUIService)
        orchestrator = self.container.resolve(IStartPositionOrchestrator)

        # Create the simplified start position picker with only 4 dependencies
        self.start_position_picker = StartPositionPicker(
            pool_manager=pool_manager,
            data_service=data_service,
            ui_service=ui_service,
            orchestrator=orchestrator,
            initial_mode=PickerMode.AUTO,  # Start in auto mode for responsive behavior
        )
        
        layout.addWidget(self.start_position_picker)
        return widget

    def _create_option_picker_widget_with_progress(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        try:

            def option_picker_progress(step: str, progress: float):
                if self.progress_callback:
                    # Map option picker progress to 76-82% range
                    mapped_progress = 76 + (progress * 6)
                    self.progress_callback(f"Option picker: {step}", mapped_progress)

            # WINDOW MANAGEMENT FIX: Create option picker during splash screen
            # Pool creation happens during splash - no window flashing due to hidden widgets
            # SIZE PROVIDER FIX: Pass widget as parent so option picker can find main window
            self.option_picker = OptionPicker(
                self.container,
                progress_callback=option_picker_progress,
                parent=widget,  # CRITICAL: Pass parent so size provider can find main window
            )
            self.option_picker.initialize()
            layout.addWidget(self.option_picker.widget)

            # WINDOW MANAGEMENT FIX: Make widgets visible after initialization
            # This prevents window flashing during splash screen
            self.option_picker.make_widgets_visible()
        except RuntimeError as e:
            print(f"❌ Failed to create option picker: {e}")
            fallback_label = QLabel("Option picker unavailable")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)
            self.option_picker = None
        return widget

    def _create_graph_editor_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        try:
            from presentation.components.graph_editor.graph_editor import GraphEditor

            self.graph_editor = GraphEditor(
                graph_service=None,
                parent=None,
                workbench_width=800,
                workbench_height=300,
            )
            layout.addWidget(self.graph_editor)
            if hasattr(self.graph_editor, "beat_modified"):
                self.graph_editor.beat_modified.connect(self._on_graph_beat_modified)
        except Exception as e:
            fallback_label = QLabel(f"Graph editor unavailable: {e}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet("color: red; font-size: 14px; padding: 20px;")
            layout.addWidget(fallback_label)
            self.graph_editor = None
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create graph editor: {e}", exc_info=True)
        return widget

    def transition_to_option_picker(self):
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(1)

    def transition_to_start_position_picker(self):
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(0)

    def transition_to_graph_editor(self):
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(2)

    def _connect_beat_frame_to_graph_editor(self):
        if not self.workbench or not self.graph_editor:
            return
        beat_frame_section = getattr(self.workbench, "_beat_frame_section", None)
        if not beat_frame_section:
            return
        beat_frame: "SequenceBeatFrame" = getattr(
            beat_frame_section, "_beat_frame", None
        )
        if not beat_frame:
            return
        beat_frame.beat_selected.connect(self._on_beat_selected_for_graph_editor)

    def _on_beat_selected_for_graph_editor(self, beat_index: int):
        # Removed repetitive debug log
        if not self.graph_editor or not self.workbench:
            print(
                f"⚠️ Missing components - graph_editor: {bool(self.graph_editor)}, workbench: {bool(self.workbench)}"
            )
            return
        current_sequence = self.workbench.get_sequence()
        if not current_sequence:
            print(f"⚠️ No current sequence available")
            return
        # Removed repetitive debug log
        if beat_index == -1:
            start_position_data = getattr(self.workbench, "_start_position_data", None)
            if start_position_data:
                self.graph_editor.set_selected_beat_data(-1, start_position_data)
            else:
                print(f"⚠️ No start position data available")
            return
        if 0 <= beat_index < len(current_sequence.beats):
            beat_data = current_sequence.beats[beat_index]
            # Removed repetitive debug log
            self.graph_editor.set_selected_beat_data(beat_index, beat_data)
        else:
            print(
                f"⚠️ Invalid beat index: {beat_index} (sequence has {len(current_sequence.beats)} beats)"
            )

    def _on_graph_beat_modified(self, beat_index: int, beat_data):
        print(f"✅ Graph editor modified beat {beat_index}")
