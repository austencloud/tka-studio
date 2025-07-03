from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QScrollArea,
    QPushButton,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from domain.models.core_models import BeatData
from application.services.data.pictograph_dataset_service import (
    PictographDatasetService,
)
from presentation.components.pictograph.pictograph_component import PictographComponent


class StartPositionOption(QWidget):
    position_selected = pyqtSignal(str)

    def __init__(self, position_key: str, grid_mode: str = "diamond"):
        super().__init__()
        self.position_key = position_key
        self.grid_mode = grid_mode
        self.dataset_service = PictographDatasetService()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.pictograph_component = PictographComponent()
        self.pictograph_component.setFixedSize(200, 200)
        self.pictograph_component.setStyleSheet(
            """
            QWidget {
                border: 2px solid rgba(255,255,255,0.25);
                border-radius: 18px;
                background: rgba(255,255,255,0.18);
            }
            QWidget:hover {
                border-color: #007bff;
                background: rgba(255,255,255,0.28);
            }
            """
        )

        beat_data = self.dataset_service.get_start_position_pictograph(
            self.position_key, self.grid_mode
        )
        if beat_data:
            self.pictograph_component.update_from_beat(beat_data)
        layout.addWidget(self.pictograph_component)
        self.setFixedSize(220, 220)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.position_selected.emit(self.position_key)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)


class StartPositionPicker(QWidget):
    start_position_selected = pyqtSignal(str)
    DIAMOND_START_POSITIONS = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
    BOX_START_POSITIONS = ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]

    def __init__(self):
        super().__init__()
        self.current_grid_mode = "diamond"
        self.position_options = []
        self._setup_ui()
        self._load_start_positions()

    def _setup_ui(self):
        self.setStyleSheet(
            """
            QWidget#GlassContainer {
                background: rgba(255,255,255,0.18);
                border-radius: 24px;
                border: 1.5px solid rgba(255,255,255,0.25);
                backdrop-filter: blur(16px);
            }
            QLabel#GlassTitle {
                color: #fff;
                background: transparent;
                text-shadow: 0 2px 8px rgba(31,38,135,0.12);
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

        # grid_toggle_layout = QHBoxLayout()
        # grid_toggle_layout.addStretch()

        diamond_btn = QPushButton("Diamond Grid")
        diamond_btn.setCheckable(True)
        diamond_btn.setChecked(True)
        diamond_btn.clicked.connect(lambda: self._set_grid_mode("diamond"))

        box_btn = QPushButton("Box Grid")
        box_btn.setCheckable(True)
        box_btn.clicked.connect(lambda: self._set_grid_mode("box"))

        # grid_toggle_layout.addWidget(diamond_btn)
        # grid_toggle_layout.addWidget(box_btn)
        # grid_toggle_layout.addStretch()
        # layout.addLayout(grid_toggle_layout)

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

    def _set_grid_mode(self, grid_mode: str):
        self.current_grid_mode = grid_mode
        self._load_start_positions()

    def _handle_position_selection(self, position_key: str):
        """Handle position selection and emit signal."""
        print(
            f"🔄 [START_POS_PICKER] _handle_position_selection called with: {position_key}"
        )
        print(f"🎯 Start position selected: {position_key}")
        print(f"🔄 [START_POS_PICKER] Emitting start_position_selected signal...")
        self.start_position_selected.emit(position_key)
        print(f"✅ [START_POS_PICKER] start_position_selected signal emitted")

    def update_layout_for_size(self, container_size):
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

    def set_grid_mode(self, grid_mode: str):
        self._set_grid_mode(grid_mode)
