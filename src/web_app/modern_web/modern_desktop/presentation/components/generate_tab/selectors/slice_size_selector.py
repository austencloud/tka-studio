"""
Slice size selector component.

Simple toggle between halved and quartered slice sizes for circular mode.
"""

from __future__ import annotations

from PyQt6.QtCore import QEvent, Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from desktop.modern.core.interfaces.generation_services import SliceSize
from desktop.modern.presentation.components.ui.pytoggle import PyToggle


class SliceSizeSelector(QWidget):
    """Simple toggle for slice size (circular mode)"""

    value_changed = pyqtSignal(SliceSize)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._current_value = SliceSize.HALVED
        self._setup_controls()

    def _setup_controls(self):
        """Setup simple slice size toggle"""
        # Main horizontal layout
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        # Left label (Halved)
        self._left_label = QLabel("Halved")
        self._left_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self._left_label.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self._left_label.installEventFilter(self)

        # Toggle switch
        self._toggle = PyToggle(
            width=60,
            bg_color="#00BCff",
            active_color="#00BCff",
            circle_color="#DDD",
            change_bg_on_state=False,
        )
        self._toggle.setChecked(False)  # Default to Halved (unchecked)
        self._toggle.stateChanged.connect(self._on_toggle_changed)

        # Right label (Quartered)
        self._right_label = QLabel("Quartered")
        self._right_label.setStyleSheet("""
            QLabel {
                color: gray;
                font-size: 14px;
                font-weight: normal;
            }
        """)
        self._right_label.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self._right_label.installEventFilter(self)

        # Add to layout
        layout.addWidget(self._left_label)
        layout.addWidget(self._toggle)
        layout.addWidget(self._right_label)

    def eventFilter(self, source, event):
        """Handle label clicks"""
        if event.type() == QEvent.Type.MouseButtonPress:
            if source == self._left_label:
                self.set_value(SliceSize.HALVED)
            elif source == self._right_label:
                self.set_value(SliceSize.QUARTERED)
            return True
        return super().eventFilter(source, event)

    def _on_toggle_changed(self, state: bool):
        """Handle toggle state change"""
        self._current_value = SliceSize.QUARTERED if state else SliceSize.HALVED
        self._update_label_styles()
        self.value_changed.emit(self._current_value)

    def _update_label_styles(self):
        """Update label styles based on current value"""
        if self._current_value == SliceSize.HALVED:
            self._left_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
            self._right_label.setStyleSheet("""
                QLabel {
                    color: gray;
                    font-size: 14px;
                    font-weight: normal;
                }
            """)
        else:
            self._left_label.setStyleSheet("""
                QLabel {
                    color: gray;
                    font-size: 14px;
                    font-weight: normal;
                }
            """)
            self._right_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)

    def set_value(self, value: SliceSize):
        """Set the current value"""
        self._current_value = value
        self._toggle.blockSignals(True)
        self._toggle.setChecked(value == SliceSize.QUARTERED)
        self._toggle.blockSignals(False)
        self._update_label_styles()

    def get_value(self) -> SliceSize:
        """Get the current value"""
        return self._current_value
