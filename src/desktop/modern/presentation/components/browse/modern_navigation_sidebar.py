"""
Modern Navigation Sidebar for Browse Tab

Provides quick navigation to different sections of the filtered results.
Based on the Legacy SequencePickerNavSidebar architecture.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class ModernNavigationSidebar(QWidget):
    """
    Modern navigation sidebar for Browse tab.

    Provides quick navigation to different sections of filtered results
    based on the current sort order (alphabetical, length, level, date).
    """

    # Signal emitted when a section is selected
    section_selected = pyqtSignal(str)  # section_name

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.current_sections: list[str] = []
        self.section_buttons: list[QPushButton] = []
        self.selected_button: QPushButton | None = None
        self.current_sort_order: str = "alphabetical"

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the navigation sidebar UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll area for navigation buttons
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # Content widget inside scroll area
        self.scroll_content = QWidget()
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(5)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # Initially show placeholder
        self._show_placeholder()

    def _show_placeholder(self) -> None:
        """Show placeholder when no sections are available."""
        placeholder = QLabel("No sections")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet(
            "color: rgba(255, 255, 255, 0.5); font-style: italic;"
        )
        self.content_layout.addWidget(placeholder)

    def _apply_styling(self) -> None:
        """Apply modern glassmorphism styling."""
        self.setStyleSheet(
            """
            ModernNavigationSidebar {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }

            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 8px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.5);
            }
        """
        )

    def update_sections(
        self, sections: list[str], sort_order: str = "alphabetical"
    ) -> None:
        """
        Update the navigation sections.

        Args:
            sections: List of section names to display
            sort_order: Current sort order (alphabetical, length, level, date_added)
        """
        self.current_sections = sections
        self.current_sort_order = sort_order

        # Clear existing content
        self._clear_content()

        if not sections:
            self._show_placeholder()
            return

        # Add section header
        header_text = self._get_header_text(sort_order)
        if header_text:
            self._add_section_header(header_text)

        # Add navigation buttons
        self._create_navigation_buttons(sections)

        # Add stretch to push buttons to top
        self.content_layout.addStretch()

    def _create_skeleton_section_button(self, section: str) -> QWidget:
        """
        Create a skeleton placeholder button for a section.

        Args:
            section: The section name (for sizing purposes)

        Returns:
            A skeleton button widget
        """
        skeleton_button = QFrame()
        skeleton_button.setFixedHeight(36)  # Same height as real buttons

        # Calculate width based on section text length
        text_width = len(section) * 8 + 24  # Approximate character width + padding
        skeleton_button.setMinimumWidth(max(60, min(120, text_width)))

        skeleton_button.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:0.5 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.08)
                );
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                margin: 2px 0px;
            }
        """
        )

        return skeleton_button

    def _get_header_text(self, sort_order: str) -> str:
        """Get the header text for the current sort order."""
        headers = {
            "alphabetical": "Letter",
            "length": "Length",
            "level": "Level",
            "date_added": "Date Added",
        }
        return headers.get(sort_order, "Sections")

    def _add_section_header(self, text: str) -> None:
        """Add a section header label."""
        header_label = QLabel(text)
        header_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                padding: 8px 5px;
                font-weight: bold;
            }
        """
        )
        self.content_layout.addWidget(header_label)

        # Add separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(
            """
            QFrame {
                background-color: rgba(255, 255, 255, 0.3);
                border: none;
                max-height: 1px;
                margin: 0px 10px;
            }
        """
        )
        self.content_layout.addWidget(separator)

    def _create_navigation_buttons(self, sections: list[str]) -> None:
        """Create navigation buttons for each section."""
        self.section_buttons.clear()

        # Handle date sections specially (like legacy system)
        if self.current_sort_order == "date_added":
            self._create_date_navigation_buttons(sections)
        else:
            # Standard navigation buttons
            for section in sections:
                button = self._create_section_button(section)
                self.section_buttons.append(button)
                self.content_layout.addWidget(button)

    def _create_date_navigation_buttons(self, sections: list[str]) -> None:
        """Create date navigation buttons grouped by year (like legacy system)."""
        # Parse dates and group by year
        parsed_dates = []
        for section in sections:
            if section == "Unknown":
                continue
            try:
                # Parse MM-DD-YYYY format
                month, day, year = section.split("-")
                parsed_dates.append((int(year), int(month), int(day), section))
            except ValueError:
                # Handle invalid date format
                button = self._create_section_button(section)
                self.section_buttons.append(button)
                self.content_layout.addWidget(button)
                continue

        # Sort by year, month, day (newest first)
        parsed_dates.sort(reverse=True, key=lambda x: (x[0], x[1], x[2]))

        # Group by year and create year headers
        current_year = None
        for year, month, day, section in parsed_dates:
            if year != current_year:
                # Add year header
                year_label = QLabel(str(year))
                year_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                year_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                year_label.setStyleSheet(
                    """
                    QLabel {
                        color: rgba(255, 255, 255, 0.9);
                        padding: 5px;
                        font-weight: bold;
                    }
                """
                )
                self.content_layout.addWidget(year_label)

                # Add year separator
                year_separator = QFrame()
                year_separator.setFrameShape(QFrame.Shape.HLine)
                year_separator.setStyleSheet(
                    """
                    QFrame {
                        background-color: rgba(255, 255, 255, 0.2);
                        border: none;
                        max-height: 1px;
                        margin: 0px 15px;
                    }
                """
                )
                self.content_layout.addWidget(year_separator)

                current_year = year

            # Create date button with formatted display (like legacy)
            display_text = f"{day}-{month}"  # Display as DD-MM
            button = self._create_section_button(display_text)
            # Store the original section name for navigation
            button.setProperty("original_section", section)
            self.section_buttons.append(button)
            self.content_layout.addWidget(button)

    def _create_section_button(self, section: str) -> QPushButton:
        """Create a styled navigation button for a section."""
        button = QPushButton(section)
        button.setFont(QFont("Segoe UI", 10))
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Apply modern button styling
        button.setStyleSheet(
            """
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.9);
                padding: 8px 12px;
                text-align: center;
                font-weight: normal;
                min-height: 20px;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.4);
                color: white;
            }

            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.25);
                border-color: rgba(255, 255, 255, 0.5);
            }
        """
        )

        # Connect click event
        button.clicked.connect(
            lambda checked, s=section: self._on_section_clicked(s, button)
        )

        return button

    def _on_section_clicked(self, section: str, button: QPushButton) -> None:
        """Handle section button click."""
        # Update button selection state
        self._update_button_selection(button)

        # For date buttons, use the original section name
        original_section = button.property("original_section")
        if original_section:
            section = original_section

        # Emit signal
        self.section_selected.emit(section)

    def _update_button_selection(self, selected_button: QPushButton) -> None:
        """Update the visual selection state of buttons."""
        # Reset previous selection
        if self.selected_button:
            self.selected_button.setStyleSheet(
                """
                QPushButton {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 8px;
                    color: rgba(255, 255, 255, 0.9);
                    padding: 8px 12px;
                    text-align: center;
                    font-weight: normal;
                    min-height: 20px;
                }

                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.2);
                    border-color: rgba(255, 255, 255, 0.4);
                    color: white;
                }

                QPushButton:pressed {
                    background: rgba(255, 255, 255, 0.25);
                    border-color: rgba(255, 255, 255, 0.5);
                }
            """
            )

        # Set new selection
        self.selected_button = selected_button
        selected_button.setStyleSheet(
            """
            QPushButton {
                background: rgba(100, 150, 255, 0.4);
                border: 1px solid rgba(100, 150, 255, 0.6);
                border-radius: 8px;
                color: white;
                padding: 8px 12px;
                text-align: center;
                font-weight: bold;
                min-height: 20px;
            }

            QPushButton:hover {
                background: rgba(100, 150, 255, 0.5);
                border-color: rgba(100, 150, 255, 0.7);
            }

            QPushButton:pressed {
                background: rgba(100, 150, 255, 0.6);
                border-color: rgba(100, 150, 255, 0.8);
            }
        """
        )

    def _clear_content(self) -> None:
        """Clear all content from the sidebar."""
        # Clear layout
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Clear button references
        self.section_buttons.clear()
        self.selected_button = None

    def resizeEvent(self, event) -> None:
        """Handle resize events to adjust button sizes."""
        super().resizeEvent(event)

        # Update button font sizes based on width
        self._update_button_fonts()

    def _update_button_fonts(self) -> None:
        """Update button font sizes based on sidebar width."""
        if not self.section_buttons:
            return

        # Calculate appropriate font size based on width
        sidebar_width = self.width()
        font_size = max(8, min(12, sidebar_width // 15))

        for button in self.section_buttons:
            font = button.font()
            font.setPointSize(font_size)
            button.setFont(font)

    def set_minimum_width(self, width: int) -> None:
        """Set the minimum width for the sidebar."""
        self.setMinimumWidth(width)
        self.setMaximumWidth(width * 2)  # Allow some flexibility

    def clear_selection(self) -> None:
        """Clear the current selection."""
        if self.selected_button:
            self._update_button_selection(None)
