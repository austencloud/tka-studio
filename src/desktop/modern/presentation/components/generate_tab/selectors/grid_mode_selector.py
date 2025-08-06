"""
Grid Mode Selector for Generate Panel

A compact control using PyToggle for selecting between Diamond and Box grid modes.
Follows the same pattern as other generation controls and uses the system PyToggle component.
"""

from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from desktop.modern.domain.models.enums import GridMode
from desktop.modern.presentation.components.ui.pytoggle import PyToggle


class ModernGridModeSelector(QWidget):
    """Compact grid mode selector using PyToggle for consistency"""

    value_changed = pyqtSignal(GridMode)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._current_mode = GridMode.DIAMOND
        self._setup_controls()

    def _setup_controls(self):
        """Setup the compact PyToggle controls."""
        from PyQt6.QtWidgets import QVBoxLayout

        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Header label
        header_label = QLabel("Grid Mode:")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-weight: 500;
            }
        """)
        main_layout.addWidget(header_label)

        # Horizontal layout for toggle controls
        control_layout = QHBoxLayout()
        control_layout.setSpacing(8)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Diamond label
        self._diamond_label = QLabel("Diamond")
        self._diamond_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._diamond_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
                border: none;
                font-size: 18px;
                font-weight: normal;
            }
        """)

        # PyToggle (Diamond=unchecked, Box=checked)
        self._toggle = PyToggle(
            width=50,  # Compact width
            bg_color="#00BCff",  # Consistent blue color
            active_color="#00BCff",  # Same blue color for consistency
            circle_color="#FFFFFF",
            animation_curve=QEasingCurve.Type.OutCubic,
            change_bg_on_state=False,  # Keep consistent color scheme
        )
        self._toggle.setChecked(False)  # Default to Diamond (unchecked)
        self._toggle.stateChanged.connect(self._on_toggle_changed)

        # Box label
        self._box_label = QLabel("Box")
        self._box_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._box_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                background: transparent;
                border: none;
                font-size: 18px;
                font-weight: normal;
            }
        """)

        # Add to horizontal layout
        control_layout.addWidget(self._diamond_label)
        control_layout.addWidget(self._toggle)
        control_layout.addWidget(self._box_label)

        # Add horizontal layout to main layout
        main_layout.addLayout(control_layout)
        self._update_label_styles()

    def _update_label_styles(self):
        """Update label styles based on current toggle state."""
        is_box_mode = self._toggle.isChecked()

        # Active label style
        active_style = """
            QLabel {
                color: rgba(255, 255, 255, 1.0);
                background: transparent;
                border: none;
                font-size: 18px;
                font-weight: bold;
            }
        """

        # Inactive label style
        inactive_style = """
            QLabel {
                color: rgba(255, 255, 255, 0.6);
                background: transparent;
                border: none;
                font-size: 18px;
                font-weight: normal;
            }
        """

        if is_box_mode:
            self._diamond_label.setStyleSheet(inactive_style)
            self._box_label.setStyleSheet(active_style)
        else:
            self._diamond_label.setStyleSheet(active_style)
            self._box_label.setStyleSheet(inactive_style)

    def _on_toggle_changed(self, checked: bool):
        """Handle toggle state change."""
        self._current_mode = GridMode.BOX if checked else GridMode.DIAMOND
        self._update_label_styles()
        self.value_changed.emit(self._current_mode)

    def set_value(self, mode: GridMode):
        """Set the grid mode value."""
        if mode != self._current_mode:
            self._current_mode = mode

            # Update toggle without triggering signals
            self._toggle.blockSignals(True)
            self._toggle.setChecked(mode == GridMode.BOX)
            self._toggle.blockSignals(False)

            # Update label styles
            self._update_label_styles()

    def reset_to_default(self):
        """Reset to default value (Diamond)."""
        self.set_value(GridMode.DIAMOND)
