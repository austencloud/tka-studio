from typing import Optional

from application.services.layout.component_sizer import ComponentSizer, SizeConstraints
from domain.models.pictograph_models import PictographData
from presentation.components.pictograph.pictograph_component import (
    PictographComponent,
    create_pictograph_component,
)
from presentation.components.workbench.sequence_beat_frame.selection_overlay import (
    SelectionOverlay,
)
from PyQt6.QtCore import QEvent, Qt, pyqtSignal
from PyQt6.QtGui import QCloseEvent, QEnterEvent, QMouseEvent
from PyQt6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout, QWidget


class ClickablePictographFrame(QFrame):
    clicked = pyqtSignal(str)
    pictograph_clicked = pyqtSignal(object)

    def __init__(
        self, pictograph_data: PictographData, parent: Optional[QWidget] = None
    ) -> None:
        if parent is not None:
            try:
                _ = parent.isVisible()
            except RuntimeError as exc:
                raise RuntimeError("Parent widget has been deleted") from exc

        super().__init__(parent)
        self.pictograph_data: PictographData = pictograph_data
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setLineWidth(0)

        self.container_widget: Optional[QWidget] = None
        self._option_picker_width: int = 0
        
        # Initialize component sizer service
        self.component_sizer = ComponentSizer()

        # Initialize selection overlay
        self._selection_overlay: Optional[SelectionOverlay] = None
        self._pictograph_component: Optional[PictographComponent] = None

        square_size: int = 160
        self.setFixedSize(square_size, square_size)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        try:
            self._pictograph_component = create_pictograph_component(parent=None)
            self.pictograph_component = (
                self._pictograph_component
            )  # Keep legacy reference
            self._pictograph_component.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

            self._configure_option_picker_context(pictograph_data)

            self._pictograph_component.update_from_pictograph_data(pictograph_data)
            layout.addWidget(self._pictograph_component)

            # Initialize selection overlay after pictograph component is set up
            self._selection_overlay = SelectionOverlay(self)

        except RuntimeError:
            fallback_label = QLabel(f"Option {pictograph_data.letter}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)
            self._pictograph_component = None
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

    def _configure_option_picker_context(self, pictograph_data: PictographData) -> None:
        if not self.pictograph_component:
            return

        try:
            from application.services.ui.pictograph_scaler import (
                ScalingContext,
            )

            self.pictograph_component.set_scaling_context(ScalingContext.OPTION_VIEW)

            if pictograph_data.glyph_data and pictograph_data.glyph_data.letter_type:
                self.pictograph_component.enable_borders()
                self.pictograph_component.update_border_colors_for_letter_type(
                    pictograph_data.glyph_data.letter_type
                )
        except Exception:
            from application.services.ui.pictograph_scaler import (
                ScalingContext,
            )

            self.pictograph_component.set_scaling_context(ScalingContext.OPTION_VIEW)
            if pictograph_data.glyph_data and pictograph_data.glyph_data.letter_type:
                self.pictograph_component.enable_borders()
                self.pictograph_component.update_border_colors_for_letter_type(
                    pictograph_data.glyph_data.letter_type
                )

    def set_container_widget(self, container_widget: QWidget) -> None:
        self.container_widget = container_widget

    def resize_frame(self) -> None:
        """Resize the frame using the ComponentSizer service."""
        try:
            if self._option_picker_width > 0:
                container_width = self._option_picker_width
            elif self.container_widget and self.container_widget.width() > 0:
                container_width = self.container_widget.width()
            else:
                return

            # Use ComponentSizer service to calculate optimal size
            constraints = SizeConstraints(
                min_size=60,
                max_size=200,
                border_width_ratio=0.015,
                spacing=3
            )
            
            final_size = self.component_sizer.calculate_pictograph_frame_size(
                container_width, constraints
            )
            
            self.setFixedSize(final_size, final_size)
        except Exception:
            # Fallback to minimum size if calculation fails
            self.setFixedSize(60, 60)

    def update_sizing_reference(self, option_picker_width: int):
        self._option_picker_width = option_picker_width
        self.resize_frame()

    def update_pictograph_data(self, pictograph_data: PictographData) -> None:
        self.pictograph_data = pictograph_data
        if self.pictograph_component:
            self._configure_option_picker_context(pictograph_data)
            self.pictograph_component.update_from_pictograph_data(pictograph_data)

    def cleanup(self) -> None:
        if self._selection_overlay:
            self._selection_overlay.hide_all()
            self._selection_overlay = None
        if self.pictograph_component:
            self.pictograph_component.cleanup()
            self.pictograph_component = None
        if self._pictograph_component:
            self._pictograph_component.cleanup()
            self._pictograph_component = None

    def closeEvent(self, event: QCloseEvent) -> None:
        self.cleanup()
        super().closeEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(f"option_{self.pictograph_data.letter}")
            self.pictograph_clicked.emit(self.pictograph_data)
        super().mousePressEvent(event)

    def set_highlighted(self, highlighted: bool) -> None:
        """Set hover state - no visual effects in legacy style"""
        pass  # No hover effects in simple legacy mode

    def set_selected(self, selected: bool) -> None:
        """Set selection state - simple legacy style"""
        if self._selection_overlay:
            if selected:
                self._selection_overlay.show_selection()
            else:
                self._selection_overlay.hide_selection()

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.set_highlighted(True)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.set_highlighted(False)
        super().leaveEvent(event)
