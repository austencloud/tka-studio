from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget


class SequenceWorkbenchButtonPanel(QWidget):
    """
    Updated button panel for sequence workbench - Save Image button REMOVED.

    The export functionality has been moved to the Export tab in the right panel
    to provide a better user experience with live preview and comprehensive settings.
    """

    # Signals for button actions - save_image_requested REMOVED
    add_to_dictionary_requested = pyqtSignal()
    # save_image_requested = pyqtSignal()  # REMOVED - Now handled by Export tab
    view_fullscreen_requested = pyqtSignal()
    mirror_sequence_requested = pyqtSignal()
    swap_colors_requested = pyqtSignal()
    rotate_sequence_requested = pyqtSignal()
    copy_json_requested = pyqtSignal()
    delete_beat_requested = pyqtSignal()
    clear_sequence_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._buttons: dict[str, QPushButton] = {}
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the button panel UI with modern layout"""
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        # Add initial stretch at the top
        layout.addStretch()

        # Button configurations with emojis for modern appeal
        button_configs = [
            # Dictionary & View group
            (
                "add_to_dictionary",
                "📚",
                "Add to Dictionary",
                self.add_to_dictionary_requested,
            ),
            # REMOVED: ("save_image", "💾", "Save Image", self.save_image_requested),
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
        button.clicked.connect(
            lambda: self._handle_button_click(signal, button.toolTip())
        )

        return button

    def _handle_button_click(self, signal, tooltip):
        """Handle button click with debug output"""
        print(f"🖱️ [BUTTON_PANEL] Button clicked: {tooltip}")
        print(f"🔄 [BUTTON_PANEL] Emitting signal: {signal}")
        signal.emit()
        print("✅ [BUTTON_PANEL] Signal emitted successfully")

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

        for _button_name, button in self._buttons.items():
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
