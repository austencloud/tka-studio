from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy, QWidget, QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QEvent
from PyQt6.QtGui import QCloseEvent, QMouseEvent, QEnterEvent
from typing import Optional

from domain.models.core_models import BeatData
from presentation.components.pictograph.pictograph_component import (
    PictographComponent,
)


class ClickablePictographFrame(QFrame):
    clicked = pyqtSignal(str)
    beat_data_clicked = pyqtSignal(object)

    def __init__(self, beat_data: BeatData, parent: Optional[QWidget] = None) -> None:
        if parent is not None:
            try:
                _ = parent.isVisible()
            except RuntimeError as exc:
                raise RuntimeError("Parent widget has been deleted") from exc

        super().__init__(parent)
        self.beat_data: BeatData = beat_data
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setLineWidth(0)

        self.container_widget: Optional[QWidget] = None
        self._option_picker_width: int = 0

        square_size: int = 160
        self.setFixedSize(square_size, square_size)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        try:
            self.pictograph_component: Optional[PictographComponent] = (
                PictographComponent(parent=None)
            )
            self.pictograph_component.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

            self._configure_option_picker_context(beat_data)

            self.pictograph_component.update_from_beat(beat_data)
            layout.addWidget(self.pictograph_component)
        except RuntimeError:
            fallback_label = QLabel(f"Beat {beat_data.letter}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)
            self.pictograph_component = None

        self.setStyleSheet(
            """
            ClickablePictographFrame {
                background-color: transparent;
                border: none;
            }
            ClickablePictographFrame:hover {
                background-color: transparent;
            }
        """
        )

        self.show()
        if self.pictograph_component:
            self.pictograph_component.show()

    def _configure_option_picker_context(self, beat_data: BeatData) -> None:
        if not self.pictograph_component:
            return

        try:
            from application.services.ui.context_aware_scaling_service import (
                ScalingContext,
            )

            self.pictograph_component.set_scaling_context(ScalingContext.OPTION_VIEW)

            if beat_data.glyph_data and beat_data.glyph_data.letter_type:
                self.pictograph_component.enable_borders()
                self.pictograph_component.update_border_colors_for_letter_type(
                    beat_data.glyph_data.letter_type
                )
        except Exception:
            from application.services.ui.context_aware_scaling_service import (
                ScalingContext,
            )

            self.pictograph_component.set_scaling_context(ScalingContext.OPTION_VIEW)
            if beat_data.glyph_data and beat_data.glyph_data.letter_type:
                self.pictograph_component.enable_borders()
                self.pictograph_component.update_border_colors_for_letter_type(
                    beat_data.glyph_data.letter_type
                )

    def set_container_widget(self, container_widget: QWidget) -> None:
        self.container_widget = container_widget

    def resize_frame(self) -> None:
        try:
            if self._option_picker_width > 0:
                container_width = self._option_picker_width
            elif self.container_widget and self.container_widget.width() > 0:
                container_width = self.container_widget.width()
            else:
                return

            container_based_size = container_width // 8
            size = container_based_size
            border_width = max(1, int(size * 0.015))
            spacing = 3
            final_size = size - (2 * border_width) - spacing
            final_size = max(60, min(final_size, 200))
            self.setFixedSize(final_size, final_size)
        except Exception:
            pass

    def update_sizing_reference(self, option_picker_width: int):
        self._option_picker_width = option_picker_width
        self.resize_frame()

    def update_beat_data(self, beat_data: BeatData) -> None:
        self.beat_data = beat_data
        if self.pictograph_component:
            self._configure_option_picker_context(beat_data)
            self.pictograph_component.update_from_beat(beat_data)

    def cleanup(self) -> None:
        if self.pictograph_component:
            self.pictograph_component.cleanup()
            self.pictograph_component = None

    def closeEvent(self, event: QCloseEvent) -> None:
        self.cleanup()
        super().closeEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(f"beat_{self.beat_data.letter}")
            self.beat_data_clicked.emit(self.beat_data)
        super().mousePressEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)
