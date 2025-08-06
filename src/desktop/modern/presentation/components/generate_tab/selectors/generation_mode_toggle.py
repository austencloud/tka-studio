"""
Generation mode toggle component.

Simple toggle between freeform and circular generation modes.
"""

from __future__ import annotations

from PyQt6.QtCore import QEvent, Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from desktop.modern.core.interfaces.generation_services import GenerationMode
from desktop.modern.presentation.components.ui.pytoggle import PyToggle


class GenerationModeToggle(QWidget):
    """Simple toggle between freeform and circular generation modes"""

    mode_changed = pyqtSignal(GenerationMode)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._current_mode = GenerationMode.FREEFORM
        self._setup_controls()

    def _setup_controls(self):
        """Setup simple mode toggle"""
        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Header label
        header_label = QLabel("Generation Mode:")
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

        # Left label (Freeform)
        self._left_label = QLabel("Freeform")
        self._left_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
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
        self._toggle.setChecked(False)  # Default to Freeform (unchecked)
        self._toggle.stateChanged.connect(self._on_toggle_changed)

        # Right label (Circular)
        self._right_label = QLabel("Circular")
        self._right_label.setStyleSheet("""
            QLabel {
                color: gray;
                font-size: 18px;
                font-weight: normal;
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
                self.set_mode(GenerationMode.FREEFORM)
            elif source == self._right_label:
                self.set_mode(GenerationMode.CIRCULAR)
            return True
        return super().eventFilter(source, event)

    def _on_toggle_changed(self, state: bool):
        """Handle toggle state change"""
        self._current_mode = (
            GenerationMode.CIRCULAR if state else GenerationMode.FREEFORM
        )
        self._update_label_styles()
        self.mode_changed.emit(self._current_mode)

    def _update_label_styles(self):
        """Update label styles based on current mode"""
        if self._current_mode == GenerationMode.FREEFORM:
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

    def set_mode(self, mode: GenerationMode):
        """Set the current mode"""
        self._current_mode = mode
        self._toggle.blockSignals(True)
        self._toggle.setChecked(mode == GenerationMode.CIRCULAR)
        self._toggle.blockSignals(False)
        self._update_label_styles()

    def get_mode(self) -> GenerationMode:
        """Get the current mode"""
        return self._current_mode
