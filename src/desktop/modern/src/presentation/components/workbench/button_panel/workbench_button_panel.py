from typing import Optional, Dict
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont


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
    edit_construct_toggle_requested = pyqtSignal(bool)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._buttons: Dict[str, QPushButton] = {}
        self._edit_mode = False  # Track current mode: False = Construct, True = Edit
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the button panel UI with modern layout"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        # Button configurations with emojis for modern appeal
        button_configs = [
            # Edit/Construct toggle (top priority)
            (
                "edit_construct_toggle",
                "✏️",
                "Edit Mode",
                self.edit_construct_toggle_requested,
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
        if button_name == "edit_construct_toggle":
            # Special handling for Edit/Construct toggle button
            button.clicked.connect(self._handle_edit_construct_toggle)
        else:
            button.clicked.connect(
                lambda: self._handle_button_click(signal, button.toolTip())
            )

        return button

    def _handle_button_click(self, signal, tooltip):
        """Handle button click with debug output"""
        print(f"🔧 DEBUG: Button clicked - {tooltip}")
        signal.emit()

    def _handle_edit_construct_toggle(self):
        """Handle Edit/Construct toggle button click"""
        self._edit_mode = not self._edit_mode
        self._update_edit_construct_button()
        self.edit_construct_toggle_requested.emit(self._edit_mode)

    def _update_edit_construct_button(self):
        """Update the Edit/Construct button appearance based on current mode"""
        if "edit_construct_toggle" in self._buttons:
            button = self._buttons["edit_construct_toggle"]
            if self._edit_mode:
                button.setText("🔧")  # Construct icon
                button.setToolTip("Construct Mode")
            else:
                button.setText("✏️")  # Edit icon
                button.setToolTip("Edit Mode")

    def _apply_styling(self):
        """Apply glassmorphism styling to the button panel and buttons"""
        # Panel glassmorphism background
        panel_style = """
            QWidget {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
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

        for button in self._buttons.values():
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
