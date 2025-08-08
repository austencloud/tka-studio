"""
Categories Section Component for Filter Selection Panel

Manages all category groups with the "Browse by Category" section.
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from application.services.browse.dictionary_data_manager import DictionaryDataManager
from desktop.modern.domain.models.browse_models import FilterType

from .category_group import CategoryGroup
from .section_title import SectionTitle


class CategoriesSection(QWidget):
    """Categories section with multiple category groups."""

    filter_selected = pyqtSignal(FilterType, object)

    def __init__(
        self,
        dictionary_manager: DictionaryDataManager,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.dictionary_manager = dictionary_manager
        self.category_groups = []
        self.all_buttons = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the categories section layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)

        # Section title
        title = SectionTitle("Browse by Category")
        title.setStyleSheet("color: rgba(255, 255, 255, 0.9); margin-bottom: 20px;")
        layout.addWidget(title)

        # Category groups
        categories = [
            (
                "📝 Name",
                FilterType.STARTING_LETTER,
                ["A-D", "E-H", "I-L", "M-P", "Q-T", "U-Z"],
            ),
            (
                "📏 Length",
                FilterType.LENGTH,
                ["3", "4", "5", "6", "8", "10"],
            ),
            (
                "📊 Difficulty",
                FilterType.DIFFICULTY,
                [
                    ("🟢 Beginner", "beginner"),
                    ("🟡 Intermediate", "intermediate"),
                    ("🔴 Advanced", "advanced"),
                ],
            ),
            (
                "🎯 Start Position",
                FilterType.STARTING_POSITION,
                ["Alpha", "Beta", "Gamma"],
            ),
            ("👤 Author", FilterType.AUTHOR, self._get_top_authors()),
            (
                "🎨 Grid Style",
                FilterType.GRID_MODE,
                [
                    ("💎 Diamond", "diamond"),
                    ("⬜ Box", "box"),
                    ("🎭 Mixed", "mixed"),
                ],
            ),
        ]

        for title_text, filter_type, options in categories:
            group = CategoryGroup(title_text, filter_type, options)
            group.filter_selected.connect(self.filter_selected.emit)
            self.category_groups.append(group)
            self.all_buttons.update(group.get_buttons())
            layout.addWidget(group)

    def _get_top_authors(self) -> list[str]:
        """Get exactly 3 authors for consistent grid."""
        try:
            authors = self.dictionary_manager.get_distinct_authors()
            # Ensure exactly 3 items for clean grid
            result = authors[:3] if len(authors) >= 3 else authors
            while len(result) < 3:
                result.append(f"Author {len(result) + 1}")
        except Exception:
            return ["Demo Author", "Test User", "Sample Creator"]
        else:
            return result

    def set_active_filter(
        self, filter_type: FilterType | None, filter_value=None
    ) -> None:
        """Set the active filter state across all groups."""
        for group in self.category_groups:
            group.set_active_filter(filter_type, filter_value)

    def get_all_buttons(self) -> dict:
        """Get all buttons from all category groups."""
        return self.all_buttons
