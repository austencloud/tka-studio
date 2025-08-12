from __future__ import annotations

import logging
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QMouseEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.domain.models import BeatData, MotionType

from .orientation_picker import OrientationPickerWidget
from ..config import ColorConfig, TurnConfig, UIConfig


logger = logging.getLogger(__name__)


class TurnAdjustButton(QPushButton):
    """Custom button that handles left/right click for different turn adjustments."""

    turn_adjusted = pyqtSignal(float)

    def __init__(self, text: str, left_click_amount: float, right_click_amount: float):
        super().__init__(text)
        self._left_click_amount = left_click_amount
        self._right_click_amount = right_click_amount
        self.setToolTip(
            f"Left click: {left_click_amount:+.2f} turn, Right click: {right_click_amount:+.2f} turn"
        )

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events for left/right click behavior."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.turn_adjusted.emit(self._left_click_amount)
        elif event.button() == Qt.MouseButton.RightButton:
            self.turn_adjusted.emit(self._right_click_amount)

        # Call parent to maintain button visual feedback
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)


class AdjustmentPanel(QWidget):
    """Legacy-exact adjustment panel implementation for graph editor."""

    beat_modified = pyqtSignal(BeatData)
    turn_applied = pyqtSignal(str, float)  # arrow_color, turn_value

    def __init__(self, parent, side: str = "right", color: str = None):
        super().__init__(parent)
        self._graph_editor = parent
        self._side = side  # "left" or "right" to match Legacy's left_stack/right_stack
        self._current_beat: Optional[BeatData] = None
        self._selected_arrow_id: Optional[str] = None

        # Determine arrow color - use provided color or derive from side
        self._arrow_color = color if color else ("blue" if side == "left" else "red")

        # Color configurations from web version
        self._color_config = self._get_color_config(self._arrow_color)

        # Create stacked widget like Legacy's QStackedLayout
        self._stacked_widget = QStackedWidget(self)

        # Add orientation picker (index 0) - like Legacy's ORI_WIDGET_INDEX
        self._orientation_picker = OrientationPickerWidget(self._arrow_color)
        self._orientation_picker.orientation_changed.connect(
            self._on_orientation_changed
        )
        self._stacked_widget.addWidget(self._orientation_picker)

        # Add existing turn controls (index 1) - like Legacy's TURNS_WIDGET_INDEX
        self._turn_controls_widget = self._create_turn_controls_widget()
        self._stacked_widget.addWidget(self._turn_controls_widget)

        # Set layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for seamless color fill
        layout.setSpacing(0)
        layout.addWidget(self._stacked_widget)

        # Apply web-inspired color-coded styling
        self._apply_color_styling()

        # UI components for turn controls (will be created in _create_turn_controls_widget)
        self._hand_indicator: Optional[QLabel] = None
        self._turn_display: Optional[QPushButton] = None
        self._decrement_button: Optional[QPushButton] = None
        self._increment_button: Optional[QPushButton] = None
        self._motion_type_label: Optional[QLabel] = None

    def _create_turn_controls_widget(self):
        """Create widget containing existing turn controls"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # 1. Hand Indicator - use color config text
        hand_text = self._color_config["text"]
        # if hand text is blue, change it to Left, if red, change it to Right
        if hand_text == "BLUE":
            hand_text = "Left"
        elif hand_text == "RED":
            hand_text = "Right"
        self._hand_indicator = QLabel(hand_text)
        self._hand_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Use primary color for text like web version
        primary_color = self._color_config["primary"]
        self._hand_indicator.setStyleSheet(
            f"color: {primary_color}; font-size: {UIConfig.HAND_INDICATOR_FONT_SIZE}px; font-weight: bold;"
        )
        layout.addWidget(self._hand_indicator)

        # 2. Turn Display - white background, colored border, clickable
        self._turn_display = QPushButton("0.0")
        self._turn_display.setFixedHeight(UIConfig.TURN_DISPLAY_HEIGHT)
        self._turn_display.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._turn_display.clicked.connect(self._on_turn_display_clicked)

        # Use color config for consistent styling
        border_color = self._color_config["border_color"]
        self._turn_display.setStyleSheet(
            f"""
            QPushButton {{
                background-color: white;
                border: 2px solid {border_color};
                border-radius: 4px;
                color: black;
                font-size: {UIConfig.TURN_DISPLAY_FONT_SIZE}px;
                font-weight: bold;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
            QPushButton:pressed {{
                background-color: #e0e0e0;
            }}
        """
        )
        layout.addWidget(self._turn_display)

        # 3. Increment/Decrement Buttons - horizontal layout
        buttons_layout = QHBoxLayout()

        # Decrement button (-) with custom mouse event handling
        self._decrement_button = TurnAdjustButton(
            "-", TurnConfig.LEFT_CLICK_DECREMENT, TurnConfig.RIGHT_CLICK_DECREMENT
        )
        self._decrement_button.setFixedSize(
            UIConfig.TURN_BUTTON_SIZE, UIConfig.TURN_BUTTON_HEIGHT
        )
        self._decrement_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._decrement_button.turn_adjusted.connect(self._adjust_turn)

        # Increment button (+) with custom mouse event handling
        self._increment_button = TurnAdjustButton(
            "+", TurnConfig.LEFT_CLICK_INCREMENT, TurnConfig.RIGHT_CLICK_INCREMENT
        )
        self._increment_button.setFixedSize(
            UIConfig.TURN_BUTTON_SIZE, UIConfig.TURN_BUTTON_HEIGHT
        )
        self._increment_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._increment_button.turn_adjusted.connect(self._adjust_turn)

        # Style both buttons
        button_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:disabled {
                background-color: rgba(100, 100, 100, 0.1);
                color: rgba(255, 255, 255, 0.3);
            }
        """
        self._decrement_button.setStyleSheet(button_style)
        self._increment_button.setStyleSheet(button_style)

        buttons_layout.addWidget(self._decrement_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self._increment_button)
        layout.addLayout(buttons_layout)

        # 4. Motion Type Display - simple text label
        self._motion_type_label = QLabel("Static")
        self._motion_type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._motion_type_label.setStyleSheet(
            f"color: white; font-size: {UIConfig.MOTION_TYPE_FONT_SIZE}px;"
        )
        layout.addWidget(self._motion_type_label)

        layout.addStretch()

        return widget

    def _get_color_config(self, color: str) -> dict:
        """Get color configuration based on web version styling"""
        if color == "blue":
            return {
                "primary": ColorConfig.BLUE_PRIMARY,
                "light": "rgba(46,49,146,0.4)",
                "medium": "rgba(46,49,146,0.8)",
                "gradient": "linear-gradient(135deg, rgba(46,49,146,0.1), rgba(46,49,146,0.8))",
                "text": "Left",
                "border_color": ColorConfig.BLUE_BORDER,
            }
        # red
        return {
            "primary": ColorConfig.RED_PRIMARY,
            "light": "rgba(237,28,36,0.4)",
            "medium": "rgba(237,28,36,0.8)",
            "gradient": "linear-gradient(135deg, rgba(237,28,36,0.1), rgba(237,28,36,0.8))",
            "text": "Right",
            "border_color": ColorConfig.RED_BORDER,
        }

    def _apply_color_styling(self):
        """Apply web-inspired color-coded styling to the adjustment panel"""
        # Create a gradient background similar to web version but adapted for Qt
        primary_color = self._color_config["primary"]

        # Convert web colors to Qt-compatible colors
        if self._arrow_color == "blue":
            light_rgba = "rgba(46, 49, 146, 102)"  # 0.4 * 255 = 102
            medium_rgba = "rgba(46, 49, 146, 204)"  # 0.8 * 255 = 204
        else:  # red
            light_rgba = "rgba(237, 28, 36, 102)"  # 0.4 * 255 = 102
            medium_rgba = "rgba(237, 28, 36, 204)"  # 0.8 * 255 = 204

        self.setStyleSheet(
            f"""
            AdjustmentPanel {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 {light_rgba},
                    stop: 0.5 {medium_rgba},
                    stop: 1 rgba(255, 255, 255, 230)
                );
                border: 4px solid {primary_color};
                border-radius: 8px;
            }}

            QLabel {{
                color: {primary_color};
                font-weight: bold;
            }}
        """
        )

    def _on_turn_display_clicked(self):
        """Handle turn display click - simplified for modern design."""
        # With modern turn controls, the turn display click can just cycle through common values
        current_turn = self._get_current_turn_value(self._arrow_color)

        # Cycle through common turn values: 0 -> 0.5 -> 1 -> 1.5 -> 2 -> 0
        common_values = [0, 0.5, 1, 1.5, 2, 2.5, 3]
        try:
            current_index = common_values.index(current_turn)
            next_index = (current_index + 1) % len(common_values)
            selected_turn = common_values[next_index]
        except ValueError:
            # If current turn is not in common values, start with 0
            selected_turn = 0

        self._apply_turn(self._arrow_color, selected_turn)
        self._update_turn_display_value(selected_turn)

    def _adjust_turn(self, amount: float):
        """Adjust turn value by the specified amount (Legacy-exact behavior)."""
        current_turn = self._get_current_turn_value(self._arrow_color)
        new_turn = max(
            TurnConfig.MIN_TURN_VALUE,
            min(TurnConfig.MAX_TURN_VALUE, current_turn + amount),
        )  # Clamp to valid range

        if new_turn != current_turn:
            self._apply_turn(self._arrow_color, new_turn)
            self._update_turn_display_value(new_turn)
            self._update_button_states(new_turn)

    def _update_button_states(self, turn_value: float):
        """Update increment/decrement button enabled states based on turn value."""
        # Disable decrement at minimum
        if self._decrement_button:
            self._decrement_button.setEnabled(turn_value > TurnConfig.MIN_TURN_VALUE)

        # Disable increment at maximum
        self._increment_button.setEnabled(turn_value < TurnConfig.MAX_TURN_VALUE)

    def _update_turn_display_value(self, turn_value: float):
        """Update the turn display with new value."""
        # Format like Legacy: show "fl" for float, otherwise show number
        if turn_value == float("inf"):
            display_text = "fl"
        else:
            display_text = str(turn_value)

        if self._turn_display:
            self._turn_display.setText(display_text)

    def _update_motion_type_display(self):
        """Update motion type label based on current beat data."""
        if not self._current_beat:
            self._motion_type_label.setText("Static")
            return

        motion = None
        if self._arrow_color == "blue" and self._current_beat.blue_motion:
            motion = self._current_beat.blue_motion
        elif self._arrow_color == "red" and self._current_beat.red_motion:
            motion = self._current_beat.red_motion

        if motion and hasattr(motion, "motion_type"):
            motion_type = motion.motion_type
            if isinstance(motion_type, MotionType):
                display_text = motion_type.value.capitalize()
            else:
                display_text = str(motion_type).capitalize()
        else:
            display_text = "Static"

        self._motion_type_label.setText(display_text)

    def _get_current_turn_value(self, arrow_color: str) -> float:
        """Get current turn value for the specified arrow color."""
        if not self._current_beat:
            return TurnConfig.MIN_TURN_VALUE

        if arrow_color == "blue" and self._current_beat.blue_motion:
            return getattr(
                self._current_beat.blue_motion, "turns", TurnConfig.MIN_TURN_VALUE
            )
        if arrow_color == "red" and self._current_beat.red_motion:
            return getattr(
                self._current_beat.red_motion, "turns", TurnConfig.MIN_TURN_VALUE
            )

        return TurnConfig.MIN_TURN_VALUE

    def _apply_turn(self, arrow_color: str, turn_value: float):
        """Apply turn value using data flow service for proper propagation"""
        if not self._current_beat:
            return

        # Use graph editor's data flow service if available
        if hasattr(self._graph_editor, "_data_flow_service"):
            updated_beat = self._graph_editor._data_flow_service.process_turn_change(
                self._current_beat, arrow_color, turn_value
            )
            self._current_beat = updated_beat
            self.turn_applied.emit(arrow_color, turn_value)
            self.beat_modified.emit(updated_beat)
        # Fallback to direct service call
        elif hasattr(self._graph_editor, "_graph_service"):
            success = self._graph_editor._graph_service.apply_turn_adjustment(
                arrow_color, turn_value
            )
            if success:
                self.turn_applied.emit(arrow_color, turn_value)
                if self._current_beat:
                    self.beat_modified.emit(self._current_beat)

    def set_beat(self, beat_data: Optional[BeatData]):
        """Enhanced panel switching with perfect beat type detection"""
        self._current_beat = beat_data

        # Determine panel mode using data flow service logic
        panel_mode = self._determine_panel_mode(beat_data)

        if panel_mode == "orientation":
            self._stacked_widget.setCurrentIndex(0)  # Show orientation picker
            self._update_orientation_picker(beat_data)
            logger.debug("Showing orientation picker for %s motion", self._arrow_color)
        else:
            self._stacked_widget.setCurrentIndex(1)  # Show turn controls
            self._update_turn_controls(beat_data)
            logger.debug("Showing turn controls for %s motion", self._arrow_color)

    def _determine_panel_mode(self, beat_data: Optional[BeatData]) -> str:
        """Determine whether to show orientation picker or turns controls"""
        if not beat_data:
            return "orientation"

        # Multiple ways to detect start position for robustness
        is_start_position = (
            # Check metadata for start position marker
            beat_data.metadata.get("is_start_position", False)
            # Check beat number (0 = start position, 1+ = regular beats)
            or getattr(beat_data, "beat_number", 1) == 0
            # Check for start position letter (α, alpha, etc.)
            or getattr(beat_data, "letter", "") in ["α", "alpha", "start"]
            # Check for sequence start position in metadata
            or "sequence_start_position" in beat_data.metadata
            # Check for static motion type (start positions are typically static)
            or (
                beat_data.blue_motion
                and beat_data.blue_motion.motion_type == MotionType.STATIC
            )
        )

        logger.debug("Panel mode detection for %s:", self._arrow_color)
        logger.debug("   Beat number: %s", getattr(beat_data, "beat_number", "None"))
        logger.debug("   Letter: %s", getattr(beat_data, "letter", "None"))
        logger.debug("   Metadata: %s", beat_data.metadata)
        logger.debug("   Is start position: %s", is_start_position)
        logger.debug(
            "   Panel mode: %s", "orientation" if is_start_position else "turns"
        )

        return "orientation" if is_start_position else "turns"

    def set_selected_arrow(self, arrow_id: str):
        """Set selected arrow and update UI highlighting."""
        self._selected_arrow_id = arrow_id

    def _update_orientation_picker(self, beat_data: BeatData):
        """Update orientation picker with beat data"""
        # Get orientation from beat data for this arrow color
        if self._arrow_color == "blue" and beat_data.blue_motion:
            orientation = getattr(beat_data.blue_motion, "orientation", "in")
        elif self._arrow_color == "red" and beat_data.red_motion:
            orientation = getattr(beat_data.red_motion, "orientation", "in")
        else:
            orientation = "in"

        self._orientation_picker.set_orientation(orientation)

    def _update_turn_controls(self, beat_data: BeatData):
        """Update turn controls with beat data"""
        self._update_ui_for_beat()

    def _on_orientation_changed(self, arrow_color: str, orientation):
        """Handle orientation change from picker"""
        if self._current_beat and hasattr(self._graph_editor, "_graph_service"):
            # Convert enum to string for service layer compatibility
            orientation_str = (
                orientation.value if hasattr(orientation, "value") else str(orientation)
            )

            # Apply orientation change through service
            success = self._graph_editor._graph_service.apply_orientation_adjustment(
                arrow_color, orientation_str
            )
            if success:
                self.beat_modified.emit(self._current_beat)

    def _update_ui_for_beat(self):
        """Update UI elements based on current beat data."""
        if not self._current_beat:
            if self._turn_display:
                self._turn_display.setText("0.0")
            if self._motion_type_label:
                self._motion_type_label.setText("Static")
            if self._turn_display:
                self._update_button_states(0.0)
            return

        # Update turn display for this panel's arrow color
        current_turn = self._get_current_turn_value(self._arrow_color)
        if self._turn_display:
            self._update_turn_display_value(current_turn)
            self._update_button_states(current_turn)

        # Update motion type display
        if self._motion_type_label:
            self._update_motion_type_display()
