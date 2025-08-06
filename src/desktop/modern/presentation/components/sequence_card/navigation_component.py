"""
Sequence Card Navigation Component

Modern implementation preserving exact legacy sidebar styling and functionality.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardDisplayService,
    ISequenceCardSettingsService,
)


logger = logging.getLogger(__name__)


class LengthOptionButton(QPushButton):
    """Custom button for length selection with selection state."""

    def __init__(self, length: int, text: str, parent=None):
        super().__init__(text, parent)
        self.length = length
        self.is_selected = False
        self.setCheckable(True)
        self._apply_styling()

    def _apply_styling(self):
        """Apply button styling."""
        self.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(71, 85, 105, 0.3), stop:1 rgba(51, 65, 85, 0.5));
                border: 1px solid rgba(100, 116, 139, 0.4);
                border-radius: 10px;
                margin: 3px;
                padding: 8px 12px;
                color: #f8fafc;
                font-weight: 500;
                text-align: center;
            }

            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 116, 139, 0.4), stop:1 rgba(71, 85, 105, 0.6));
                border: 1px solid rgba(148, 163, 184, 0.5);
            }

            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                border: 1px solid #60a5fa;
                color: white;
                font-weight: 600;
            }
        """
        )

    def setSelected(self, selected: bool):
        """Set selection state."""
        self.is_selected = selected
        self.setChecked(selected)


class SequenceCardNavigationComponent(QWidget):
    """Navigation component with exact legacy sidebar styling preserved."""

    length_selected = pyqtSignal(int)
    column_count_changed = pyqtSignal(int)

    def __init__(
        self,
        settings_service: ISequenceCardSettingsService,
        display_service: ISequenceCardDisplayService,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.settings_service = settings_service
        self.display_service = display_service

        self.length_buttons = {}
        self.selected_length = 16  # Default

        self._setup_ui()
        self._apply_legacy_styling()
        self._setup_connections()
        self._load_saved_settings()

    def _setup_ui(self) -> None:
        """Setup navigation UI with exact legacy layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)

        # Header section
        self.header = self._create_sidebar_header()
        main_layout.addWidget(self.header)

        # Length selection scroll area
        self.length_scroll_area = self._create_length_scroll_area()
        main_layout.addWidget(self.length_scroll_area, 1)

        # Column selector
        self.column_selector = self._create_column_selector()
        main_layout.addWidget(self.column_selector)

    def _create_sidebar_header(self) -> QFrame:
        """Create the sidebar header."""
        header = QFrame()
        header.setObjectName("sidebarHeader")

        layout = QVBoxLayout(header)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(4)

        # Title
        title = QLabel("Sequence Length")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.5)
        title.setFont(title_font)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Select a length to display")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_font.setItalic(True)
        subtitle.setFont(subtitle_font)
        layout.addWidget(subtitle)

        return header

    def _create_length_scroll_area(self) -> QScrollArea:
        """Create the length selection scroll area."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setSpacing(5)

        # Length options - exact legacy order
        length_options = [
            (0, "All"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
            (6, "6"),
            (8, "8"),
            (10, "10"),
            (12, "12"),
            (16, "16"),
        ]

        for length, text in length_options:
            button = LengthOptionButton(length, text)
            button.clicked.connect(
                lambda checked, l=length: self._on_length_button_clicked(l)
            )
            self.length_buttons[length] = button
            content_layout.addWidget(button)

        content_layout.addStretch()
        scroll_area.setWidget(content_widget)

        return scroll_area

    def _create_column_selector(self) -> QFrame:
        """Create the column selector."""
        selector_frame = QFrame()
        selector_frame.setObjectName("columnSelector")

        layout = QVBoxLayout(selector_frame)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        # Label
        label = QLabel("Preview Columns:")
        label_font = QFont()
        label_font.setPointSize(12)
        label_font.setWeight(QFont.Weight.Medium)
        label.setFont(label_font)
        layout.addWidget(label)

        # Combo box
        self.column_combo = QComboBox()
        self.column_combo.addItems(["2", "3", "4", "5", "6"])
        self.column_combo.setCurrentText("2")  # Default
        layout.addWidget(self.column_combo)

        return selector_frame

    def _apply_legacy_styling(self) -> None:
        """Apply exact legacy styling."""
        self.setObjectName("sequenceCardNavigation")
        self.setStyleSheet(
            """
            #sequenceCardNavigation {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(71, 85, 105, 0.4), stop:1 rgba(51, 65, 85, 0.6));
                border-radius: 12px;
                border: 1px solid rgba(100, 116, 139, 0.3);
            }

            #sidebarHeader {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(71, 85, 105, 0.5), stop:1 rgba(51, 65, 85, 0.7));
                border-radius: 10px;
                border: 1px solid rgba(100, 116, 139, 0.4);
            }

            #sidebarHeader QLabel {
                color: #f8fafc;
                font-weight: bold;
            }

            #columnSelector {
                background: rgba(71, 85, 105, 0.3);
                border-radius: 8px;
                border: 1px solid rgba(100, 116, 139, 0.4);
            }

            #columnSelector QLabel {
                color: #f8fafc;
                font-weight: medium;
            }

            QComboBox {
                background: rgba(71, 85, 105, 0.6);
                border: 1px solid rgba(100, 116, 139, 0.5);
                border-radius: 8px;
                padding: 6px 10px;
                color: #f8fafc;
                font-size: 12px;
                min-height: 20px;
            }

            QComboBox::drop-down {
                border: none;
                width: 20px;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #f8fafc;
                margin-right: 5px;
            }

            QComboBox QAbstractItemView {
                background: rgba(71, 85, 105, 0.9);
                border: 1px solid rgba(100, 116, 139, 0.5);
                border-radius: 6px;
                color: #f8fafc;
                selection-background-color: rgba(59, 130, 246, 0.6);
            }

            QScrollArea {
                border: none;
                background: transparent;
            }

            QScrollBar:vertical {
                background: rgba(0, 0, 0, 0.1);
                width: 8px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 4px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.5);
            }
        """
        )

    def _setup_connections(self) -> None:
        """Setup signal connections."""
        self.column_combo.currentTextChanged.connect(self._on_column_count_changed)

    def _load_saved_settings(self) -> None:
        """Load saved settings."""
        try:
            # Load saved length
            saved_length = self.settings_service.get_last_selected_length()
            self.select_length(saved_length)

            # Load saved column count
            saved_columns = self.settings_service.get_column_count()
            self.column_combo.setCurrentText(str(saved_columns))

        except Exception as e:
            logger.warning(f"Error loading saved settings: {e}")

    def _on_length_button_clicked(self, length: int) -> None:
        """Handle length button click."""
        # Update selection state
        for button_length, button in self.length_buttons.items():
            button.setSelected(button_length == length)

        self.selected_length = length
        logger.info(f"Length selected: {length}")
        self.length_selected.emit(length)

    def _on_column_count_changed(self, count_text: str) -> None:
        """Handle column count change."""
        try:
            count = int(count_text)
            logger.info(f"Column count changed: {count}")
            self.column_count_changed.emit(count)
        except ValueError:
            logger.warning(f"Invalid column count: {count_text}")

    def select_length(self, length: int) -> None:
        """Programmatically select a length."""
        if length in self.length_buttons:
            self._on_length_button_clicked(length)
        else:
            logger.warning(f"Invalid length selection: {length}")

    def resizeEvent(self, event) -> None:
        """Handle resize event for responsive font scaling."""
        super().resizeEvent(event)

        # Update font sizes based on width (legacy behavior)
        new_width = event.size().width()

        for button in self.length_buttons.values():
            font = button.font()
            new_size = min(max(12, int(new_width / 15)), 14)
            font.setPointSize(new_size)
            button.setFont(font)
