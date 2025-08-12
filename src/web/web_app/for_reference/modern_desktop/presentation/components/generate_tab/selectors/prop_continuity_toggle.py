"""
Prop continuity toggle component.

Simple toggle between random and continuous prop behavior.
"""

from __future__ import annotations

from PyQt6.QtCore import QEvent, Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from desktop.modern.core.interfaces.generation_services import PropContinuity
from desktop.modern.presentation.components.ui.pytoggle import PyToggle


class PropContinuityToggle(QWidget):
    """Simple toggle for prop continuity setting"""

    value_changed = pyqtSignal(PropContinuity)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._current_value = PropContinuity.CONTINUOUS
        self._setup_controls()

    def _setup_controls(self):
        """Setup simple prop continuity toggle"""
        from PyQt6.QtWidgets import QVBoxLayout

        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Header label
        header_label = QLabel("Prop Continuity:")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: 500;
            }
        """)
        main_layout.addWidget(header_label)

        # Horizontal layout for toggle controls
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        # Left label (Random)
        self._left_label = QLabel("Random")
        self._left_label.setStyleSheet("""
            QLabel {
                color: gray;
                font-size: 18px;
                font-weight: normal;
                background: transparent;
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
        self._toggle.setChecked(True)  # Default to Continuous (checked)
        self._toggle.stateChanged.connect(self._on_toggle_changed)

        # Right label (Continuous)
        self._right_label = QLabel("Continuous")
        self._right_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
            }
        """)
        self._right_label.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self._right_label.installEventFilter(self)

        # Add to horizontal layout
        layout.addWidget(self._left_label)
        layout.addWidget(self._toggle)
        layout.addWidget(self._right_label)

        # Add horizontal layout to main layout
        main_layout.addLayout(layout)

    def eventFilter(self, source, event):
        """Handle label clicks"""
        if event.type() == QEvent.Type.MouseButtonPress:
            if source == self._left_label:
                self.set_value(PropContinuity.RANDOM)
            elif source == self._right_label:
                self.set_value(PropContinuity.CONTINUOUS)
            return True
        return super().eventFilter(source, event)

    def _on_toggle_changed(self, state: bool):
        """Handle toggle state change"""
        self._current_value = (
            PropContinuity.CONTINUOUS if state else PropContinuity.RANDOM
        )
        self._update_label_styles()
        self.value_changed.emit(self._current_value)

    def _update_label_styles(self):
        """Update label styles based on current value"""
        if self._current_value == PropContinuity.RANDOM:
            self._left_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    background: transparent;
                }
            """)
            self._right_label.setStyleSheet("""
                QLabel {
                    color: gray;
                    font-size: 18px;
                    font-weight: normal;
                    background: transparent;
                }
            """)
        else:
            self._left_label.setStyleSheet("""
                QLabel {
                    color: gray;
                    font-size: 18px;
                    font-weight: normal;
                    background: transparent;
                }
            """)
            self._right_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    background: transparent;
                }
            """)

    def set_value(self, value: PropContinuity):
        """Set the current value"""
        self._current_value = value
        self._toggle.blockSignals(True)
        self._toggle.setChecked(value == PropContinuity.CONTINUOUS)
        self._toggle.blockSignals(False)
        self._update_label_styles()

    def get_value(self) -> PropContinuity:
        """Get the current value"""
        return self._current_value
