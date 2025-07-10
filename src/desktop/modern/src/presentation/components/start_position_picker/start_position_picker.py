from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QScrollArea,
    QPushButton,
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QFont

# Remove unused import that was causing the module error
# from application.services.data.pictograph_dataset_service import (
#     PictographDatasetService,
# )
from presentation.components.pictograph.pictograph_component import PictographComponent
from presentation.components.start_position_picker.start_position_option import (
    StartPositionOption,
)
from presentation.components.workbench.sequence_beat_frame.selection_overlay import (
    SelectionOverlay,
)

# Import for command-based architecture
import logging

logger = logging.getLogger(__name__)


class StartPositionPicker(QWidget):
    start_position_selected = pyqtSignal(str)
    DIAMOND_START_POSITIONS = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
    BOX_START_POSITIONS = ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]

    def __init__(self):
        super().__init__()
        self.current_grid_mode = "diamond"
        self.position_options: list[StartPositionOption] = []
        self._setup_ui()
        self._load_start_positions()

    def _setup_ui(self):
        self.setStyleSheet(
            """
            QWidget#GlassContainer {
                background: rgba(255,255,255,0.18);
                border-radius: 24px;
                border: 1.5px solid rgba(255,255,255,0.25);
            }
            QLabel#GlassTitle {
                color: #fff;
                background: transparent;
            }
            QLabel#GlassInstructions {
                color: #e2e8f0;
                background: transparent;
            }
            QPushButton {
                background: rgba(255,255,255,0.22);
                border: 1.5px solid rgba(255,255,255,0.25);
                border-radius: 12px;
                color: #2d3748;
                font-weight: 600;
                padding: 6px 18px;
            }
            QPushButton:checked {
                background: rgba(0,123,255,0.18);
                color: #007bff;
                border-color: #007bff;
            }
            """
        )
        self.setObjectName("GlassContainer")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title = QLabel("Choose Your Start Position")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("GlassTitle")
        layout.addWidget(title)

        instructions = QLabel(
            "Select a starting position to begin building your sequence."
        )
        instructions.setFont(QFont("Arial", 12))
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setObjectName("GlassInstructions")
        layout.addWidget(instructions)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.positions_container = QWidget()
        self.positions_layout = QGridLayout(self.positions_container)
        self.positions_layout.setSpacing(15)

        scroll_area.setWidget(self.positions_container)
        layout.addWidget(scroll_area)

    def _load_start_positions(self):
        for option in self.position_options:
            option.setParent(None)
        self.position_options.clear()
        position_keys = (
            self.DIAMOND_START_POSITIONS
            if self.current_grid_mode == "diamond"
            else self.BOX_START_POSITIONS
        )
        for i, position_key in enumerate(position_keys):
            option = StartPositionOption(position_key, self.current_grid_mode)
            option.position_selected.connect(self._handle_position_selection)
            row = i // 3
            col = i % 3
            self.positions_layout.addWidget(option, row, col)
            self.position_options.append(option)

    def _handle_position_selection(self, position_key: str):
        """Handle position selection via command pattern."""
        try:
            # Import command and services
            from core.commands.start_position_commands import SetStartPositionCommand
            from core.service_locator import get_command_processor, get_event_bus

            # Get services
            command_processor = get_command_processor()
            event_bus = get_event_bus()

            if not command_processor or not event_bus:
                print(
                    "⚠️ Command processor or event bus not available, falling back to signal"
                )
                self.start_position_selected.emit(position_key)
                return

            # Create and execute command
            command = SetStartPositionCommand(
                position_key=position_key, event_bus=event_bus
            )

            result = command_processor.execute(command)

            if result.success:
                print(f"✅ Start position set via command: {position_key}")
                # Still emit signal for UI transition (option picker)
                self.start_position_selected.emit(position_key)
            else:
                print(f"❌ Failed to set start position: {result.error_message}")
                # TODO: Show error to user

        except Exception as e:
            print(f"❌ Error in start position selection: {e}")
            # Fallback to original behavior
            self.start_position_selected.emit(position_key)

    def update_layout_for_size(self, container_size: QSize):
        if not self.position_options:
            return
        container_width = container_size.width()
        total_positions = len(self.position_options)
        position_width = 220
        total_width_needed = (
            total_positions * position_width + (total_positions - 1) * 15
        )
        for i in reversed(range(self.positions_layout.count())):
            item = self.positions_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)
        if container_width >= total_width_needed + 100:
            for i, option in enumerate(self.position_options):
                self.positions_layout.addWidget(option, 0, i)
        else:
            max_cols = max(1, (container_width - 100) // (position_width + 15))
            for i, option in enumerate(self.position_options):
                row = i // max_cols
                col = i % max_cols
                self.positions_layout.addWidget(option, row, col)
        self.positions_container.update()

    def get_current_grid_mode(self) -> str:
        return self.current_grid_mode
