from enum import Enum
from typing import Dict, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget


class RightPanelMode(Enum):
    """Right panel display modes."""

    PICKER = "picker"  # Option/Start Position Picker (smart switching)
    GRAPH_EDITOR = "graph"  # Graph Editor
    GENERATE = "generate"  # Generate Controls


class SequenceWorkbenchButtonPanel(QWidget):
    """Modern button panel for sequence workbench with glassmorphism styling and signals"""

    # Signals for button actions
    add_to_dictionary_requested = pyqtSignal()
    save_image_requested = pyqtSignal()
    view_fullscreen_requested = pyqtSignal()
    mirror_sequence_requested = pyqtSignal()
    swap_colors_requested = pyqtSignal()
    rotate_sequence_requested = pyqtSignal()
    copy_json_requested = pyqtSignal()
    delete_beat_requested = pyqtSignal()
    clear_sequence_requested = pyqtSignal()

    # New signals for 3-panel system
    right_panel_mode_requested = pyqtSignal(str)  # RightPanelMode.value
    picker_mode_requested = pyqtSignal()  # Smart picker (option or start pos)
    graph_editor_requested = pyqtSignal()  # Graph editor
    generate_requested = pyqtSignal()  # Generate controls

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._buttons: Dict[str, QPushButton] = {}
        self._current_panel_mode = RightPanelMode.PICKER  # Track current panel mode
        self._has_sequence = False  # Track if sequence exists for smart button text
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the button panel UI with modern layout"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        # Button configurations with emojis for modern appeal
        button_configs = [
            # Right Panel Mode Selectors (top priority)
            (
                "picker_mode",
                "🔨",
                "Start Position Picker",
                None,  # Special handling
            ),
            (
                "graph_editor_mode",
                "🔧",
                "Graph Editor",
                None,  # Special handling
            ),
            (
                "generate_mode",
                "🤖",
                "Generate Controls",
                None,  # Special handling
            ),
            # Spacer
            None,
            # Dictionary & Export group
            (
                "add_to_dictionary",
                "📚",
                "Add to Dictionary",
                self.add_to_dictionary_requested,
            ),
            ("save_image", "💾", "Save Image", self.save_image_requested),
            (
                "view_fullscreen",
                "👁️",
                "View Fullscreen",
                self.view_fullscreen_requested,
            ),
            # Spacer
            None,
            # Transform group
            (
                "mirror_sequence",
                "🪞",
                "Mirror Sequence",
                self.mirror_sequence_requested,
            ),
            ("swap_colors", "🎨", "Swap Colors", self.swap_colors_requested),
            (
                "rotate_sequence",
                "🔄",
                "Rotate Sequence",
                self.rotate_sequence_requested,
            ),
            # Spacer
            None,
            # Sequence management group
            ("copy_json", "📋", "Copy JSON", self.copy_json_requested),
            ("delete_beat", "🗑️", "Delete Beat", self.delete_beat_requested),
            ("clear_sequence", "🧹", "Clear Sequence", self.clear_sequence_requested),
        ]

        for config in button_configs:
            if config is None:
                # Add spacer between groups
                spacer = QSpacerItem(
                    20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
                )
                layout.addItem(spacer)
            else:
                button_name, emoji, tooltip, signal = config
                button = self._create_button(button_name, emoji, tooltip, signal)
                self._buttons[button_name] = button
                layout.addWidget(button)

        # Add final stretch
        layout.addStretch()

    def _create_button(
        self, button_name: str, emoji: str, tooltip: str, signal: pyqtSignal
    ) -> QPushButton:
        """Create a modern button with emoji and signal connection"""
        button = QPushButton(emoji)
        button.setToolTip(tooltip)
        button.setMinimumSize(48, 48)
        button.setMaximumSize(48, 48)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Set font for emoji
        font = QFont()
        font.setPointSize(16)
        button.setFont(font)

        # Connect to signal
        if button_name == "picker_mode":
            button.setCheckable(True)
            button.clicked.connect(self._handle_picker_mode_clicked)
        elif button_name == "graph_editor_mode":
            button.setCheckable(True)
            button.clicked.connect(self._handle_graph_editor_clicked)
        elif button_name == "generate_mode":
            button.setCheckable(True)
            button.clicked.connect(self._handle_generate_clicked)
        else:
            button.clicked.connect(
                lambda: self._handle_button_click(signal, button.toolTip())
            )

        return button

    def _handle_button_click(self, signal, tooltip):
        """Handle button click with debug output"""
        print(f"🖱️ [BUTTON_PANEL] Button clicked: {tooltip}")
        print(f"🔄 [BUTTON_PANEL] Emitting signal: {signal}")
        signal.emit()
        print(f"✅ [BUTTON_PANEL] Signal emitted successfully")

    def _handle_picker_mode_clicked(self):
        """Handle picker mode button click - smart switching based on sequence state."""
        print(f"🎯 [BUTTON_PANEL] Picker mode requested")
        self._set_current_panel_mode(RightPanelMode.PICKER)
        self.picker_mode_requested.emit()
        self.right_panel_mode_requested.emit(RightPanelMode.PICKER.value)

    def _handle_graph_editor_clicked(self):
        """Handle graph editor button click."""
        print(f"📊 [BUTTON_PANEL] Graph editor requested")
        self._set_current_panel_mode(RightPanelMode.GRAPH_EDITOR)
        self.graph_editor_requested.emit()
        self.right_panel_mode_requested.emit(RightPanelMode.GRAPH_EDITOR.value)

    def _handle_generate_clicked(self):
        """Handle generate controls button click."""
        print(f"🤖 [BUTTON_PANEL] Generate controls requested")
        self._set_current_panel_mode(RightPanelMode.GENERATE)
        self.generate_requested.emit()
        self.right_panel_mode_requested.emit(RightPanelMode.GENERATE.value)

    def _set_current_panel_mode(self, mode: RightPanelMode):
        """Set the current panel mode and update button states."""
        if mode != self._current_panel_mode:
            self._current_panel_mode = mode
            self._update_panel_button_states()

    def _update_panel_button_states(self):
        """Update panel button visual states based on current mode."""
        panel_buttons = {
            RightPanelMode.PICKER: "picker_mode",
            RightPanelMode.GRAPH_EDITOR: "graph_editor_mode",
            RightPanelMode.GENERATE: "generate_mode",
        }

        for mode, button_name in panel_buttons.items():
            if button_name in self._buttons:
                button = self._buttons[button_name]
                is_active = mode == self._current_panel_mode
                button.setChecked(is_active)

                # Update button styling based on state
                if is_active:
                    button.setStyleSheet(self._get_active_panel_button_style())
                else:
                    button.setStyleSheet(self._get_inactive_panel_button_style())

    def set_sequence_state(self, has_sequence: bool, has_start_position: bool = False):
        """
        Update the picker button text based on sequence state.

        Args:
            has_sequence: True if a sequence exists
            has_start_position: True if a start position is set
        """
        self._has_sequence = has_sequence

        # Update picker button tooltip based on state
        if "picker_mode" in self._buttons:
            picker_button = self._buttons["picker_mode"]

            if not has_start_position:
                # No start position set - show start position picker
                picker_button.setToolTip("Start Position Picker")
                picker_button.setText("🎯")  # Target for start position
            elif not has_sequence:
                # Start position set but no sequence - show option picker
                picker_button.setToolTip("Option Picker")
                picker_button.setText("⚡")  # Lightning for options/moves
            else:
                # Full sequence exists - show option picker for next moves
                picker_button.setToolTip("Option Picker")
                picker_button.setText("⚡")  # Lightning for options/moves

    def get_current_panel_mode(self) -> RightPanelMode:
        """Get the currently selected panel mode."""
        return self._current_panel_mode

    def set_panel_mode(self, mode: RightPanelMode):
        """Programmatically set the panel mode (e.g., from external state changes)."""
        self._set_current_panel_mode(mode)

    def reset_to_picker_mode(self):
        """Reset to picker mode (called when sequence is cleared)"""
        print("🔄 [BUTTON_PANEL] Resetting to picker mode after sequence clear")
        self._set_current_panel_mode(RightPanelMode.PICKER)
        self.set_sequence_state(False, False)  # No sequence, no start position

    def _apply_styling(self):
        """Apply glassmorphism styling to the button panel and buttons, with a black border"""
        # Panel glassmorphism background with visible black border
        panel_style = """
            QWidget {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid black;
                border-radius: 12px;
            }
        """
        self.setStyleSheet(panel_style)

        # Button glassmorphism styling
        button_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                color: #2C3E50;
                font-weight: 500;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.35);
            }
            QPushButton:disabled {
                background: rgba(200, 200, 200, 0.1);
                border: 1px solid rgba(200, 200, 200, 0.2);
                color: #BDC3C7;
            }
        """

        for button_name, button in self._buttons.items():
            # Panel mode buttons get special styling
            if button_name in ["picker_mode", "graph_editor_mode", "generate_mode"]:
                if button.isChecked():
                    button.setStyleSheet(self._get_active_panel_button_style())
                else:
                    button.setStyleSheet(self._get_inactive_panel_button_style())
            else:
                button.setStyleSheet(button_style)

    def set_button_enabled(self, button_name: str, enabled: bool):
        """Enable or disable a specific button"""
        if button_name in self._buttons:
            self._buttons[button_name].setEnabled(enabled)

    def show_message_tooltip(
        self, button_name: str, message: str, duration: int = 2000
    ):
        """Show a temporary message on a button tooltip"""
        if button_name in self._buttons:
            button = self._buttons[button_name]
            original_tooltip = button.toolTip()
            button.setToolTip(message)

            # Reset tooltip after duration (simplified for now)
            # In a full implementation, you'd use QTimer for this
            button.setToolTip(original_tooltip)

    def update_button_sizes(self, container_height: int):
        """Update button sizes for responsive design"""
        # Calculate button size based on container height
        button_size = max(32, min(64, container_height // 15))
        font_size = max(12, min(20, button_size // 3))

        for button in self._buttons.values():
            button.setMinimumSize(button_size, button_size)
            button.setMaximumSize(button_size, button_size)

            # Update font size
            font = button.font()
            font.setPointSize(font_size)
            button.setFont(font)

    def _get_active_panel_button_style(self) -> str:
        """Get styling for active/selected panel button."""
        return """
            QPushButton {
                background: rgba(70, 130, 180, 0.3);
                border: 2px solid rgba(70, 130, 180, 0.6);
                border-radius: 8px;
                color: #1e3a8a;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(70, 130, 180, 0.4);
                border: 2px solid rgba(70, 130, 180, 0.8);
            }
            QPushButton:pressed {
                background: rgba(70, 130, 180, 0.5);
            }
        """

    def _get_inactive_panel_button_style(self) -> str:
        """Get styling for inactive panel button."""
        return """
            QPushButton {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                color: #2C3E50;
                font-weight: 500;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.35);
            }
        """
