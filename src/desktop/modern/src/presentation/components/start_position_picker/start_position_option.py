from application.services.data.dataset_query import DatasetQuery
from presentation.components.pictograph.pictograph_component import (
    create_pictograph_component,
)
from presentation.components.workbench.sequence_beat_frame.selection_overlay import (
    SelectionOverlay,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)


class StartPositionOption(QWidget):
    position_selected = pyqtSignal(str)

    def __init__(self, position_key: str, grid_mode: str = "diamond"):
        super().__init__()
        self.position_key = position_key
        self.grid_mode = grid_mode
        self.dataset_service = DatasetQuery()

        # Initialize selection overlay components
        self._pictograph_component = None
        self._selection_overlay = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self._pictograph_component = create_pictograph_component()
        self.pictograph_component = self._pictograph_component  # Keep legacy reference
        self._pictograph_component.setFixedSize(200, 200)

        self._pictograph_component.setStyleSheet(
            """
            QWidget {
                border: 2px solid rgba(255,255,255,0.25);
                border-radius: 18px;
                background: rgba(255,255,255,0.18);
            }
            """
        )

        pictograph_data = self.dataset_service.get_start_position_pictograph_data(
            self.position_key, self.grid_mode
        )
        if pictograph_data:
            self._pictograph_component.update_from_pictograph_data(pictograph_data)
        layout.addWidget(self._pictograph_component)

        self._selection_overlay = SelectionOverlay(self)

        self.setFixedSize(220, 220)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event: "QMouseEvent"):
        if event.button() == Qt.MouseButton.LeftButton:
            self.position_selected.emit(self.position_key)
        super().mousePressEvent(event)

    def set_highlighted(self, highlighted: bool) -> None:
        """Set hover state with scaling compensation"""
        if self._selection_overlay:
            if highlighted:
                self._selection_overlay.show_hover()
            else:
                self._selection_overlay.hide_hover_only()

    def set_selected(self, selected: bool) -> None:
        """Set selection state with scaling compensation"""
        if self._selection_overlay:
            if selected:
                self._selection_overlay.show_selection()
            else:
                self._selection_overlay.hide_all()

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.set_highlighted(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.set_highlighted(False)
        super().leaveEvent(event)
