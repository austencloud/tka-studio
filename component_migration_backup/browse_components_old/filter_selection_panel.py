"""
Filter Selection Panel - Modern Organized Layout

Features:
- Quick access section for common filters (Favorites, Recent, All)
- Organized category sections in 2x3 grid layout
- Glass-morphism styling with modern 2025 design
- Responsive design that adapts to container size
- Maintains all existing filter functionality
"""

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.application.services.browse.browse_service import (
    BrowseService,
)
from desktop.modern.application.services.browse.modern_dictionary_data_manager import (
    ModernDictionaryDataManager,
)
from desktop.modern.presentation.components.browse.filter_sections import (
    FilterCategorySection,
    QuickAccessSection,
)
from desktop.modern.presentation.styles.core.types import ComponentType, StyleVariant

# Import design system for consistent styling
from desktop.modern.presentation.styles.mixins import StyleMixin, apply_style_to_widget
from desktop.modern.presentation.views.browse.models import FilterType


class FilterSelectionPanel(QWidget, StyleMixin):
    """
    Modern organized filter selection interface.

    Replaces the overwhelming 3x3 grid with organized sections:
    - Quick Access: Favorites, Recent, All (prominent)
    - Categories: Name, Length, Difficulty, Position, Author, Grid Mode
    """

    # Signals
    filter_selected = pyqtSignal(FilterType, object)

    def __init__(
        self,
        browse_service: BrowseService,
        dictionary_manager: ModernDictionaryDataManager,
        parent: QWidget | None = None,
    ):
        """Initialize the organized filter selection panel."""
        super().__init__(parent)

        self.browse_service = browse_service
        self.dictionary_manager = dictionary_manager
        self._category_columns = 2  # Default 2 columns for categories
        self._layout_initialized = False

        self._setup_ui()
        self._connect_signals()

        # Defer final layout initialization
        QTimer.singleShot(100, self._finalize_layout_initialization)

    def _setup_ui(self) -> None:
        """Setup the organized UI layout."""
        # Create scroll area for responsive design
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        # Main content widget
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)

        # Main layout
        self.main_layout = QVBoxLayout(content_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(24)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header
        self._setup_header()

        # Quick Access Section
        self._setup_quick_access()

        # Category Sections
        self._setup_category_sections()

        # Set up scroll area in widget layout
        widget_layout = QVBoxLayout(self)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.addWidget(scroll_area)

        # Apply container styling
        self._apply_container_styling()

    def _setup_header(self) -> None:
        """Setup the header section."""
        header_layout = QHBoxLayout()

        # Title
        self.title_label = QLabel("TKA Sequence Library")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        self.title_label.setFont(title_font)

        # Apply centralized label styling using design system
        apply_style_to_widget(
            self.title_label,
            ComponentType.LABEL,
            StyleVariant.ACCENT,
            size="3xl",
            weight="bold",
        )

        header_layout.addWidget(self.title_label)
        self.main_layout.addLayout(header_layout)

    def _setup_quick_access(self) -> None:
        """Setup the quick access section."""
        # Quick access title
        quick_title = QLabel("Quick Access")
        quick_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        quick_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        quick_title.setFont(quick_font)

        # Apply centralized label styling
        apply_style_to_widget(
            quick_title,
            ComponentType.LABEL,
            StyleVariant.PROMINENT,
            size="2xl",
            weight="bold",
        )
        self.main_layout.addWidget(quick_title)

        # Quick access section
        self.quick_access = QuickAccessSection()
        self.main_layout.addWidget(self.quick_access)

    def _setup_category_sections(self) -> None:
        """Setup the organized category sections."""
        # Categories title
        categories_title = QLabel("Browse by Category")
        categories_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        categories_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        categories_title.setFont(categories_font)

        # Apply centralized label styling
        apply_style_to_widget(
            categories_title,
            ComponentType.LABEL,
            StyleVariant.PROMINENT,
            size="2xl",
            weight="bold",
        )
        self.main_layout.addWidget(categories_title)

        # Categories grid container
        self.categories_container = QWidget()
        self.categories_layout = QGridLayout(self.categories_container)
        self.categories_layout.setSpacing(16)
        self.categories_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create category sections
        self._create_category_sections()

        self.main_layout.addWidget(self.categories_container)

    def _create_category_sections(self) -> None:
        """Create all the category sections."""
        # Define categories with their configurations
        categories = [
            # Name-based filters
            (
                "📝 By Sequence Name",
                FilterType.STARTING_LETTER,
                ["A-D", "E-H", "I-L", "M-P", "Q-T", "U-Z", "All Letters"],
                3,  # 3 columns for name options
            ),
            # Length-based filters
            (
                "📏 By Length",
                FilterType.LENGTH,
                ["3", "4", "5", "6", "8", "10", "12", "16", "All"],
                3,  # 3 columns for length options
            ),
            # Difficulty-based filters (with colors)
            (
                "📊 By Difficulty",
                FilterType.DIFFICULTY,
                [
                    ("🟢 Beginner", "beginner", "#4CAF50"),
                    ("🟡 Intermediate", "intermediate", "#FF9800"),
                    ("🔴 Advanced", "advanced", "#F44336"),
                    ("All Levels", "all", None),
                ],
                2,  # 2 columns for difficulty
            ),
            # Position-based filters
            (
                "🎯 By Start Position",
                FilterType.STARTING_POSITION,
                ["Alpha", "Beta", "Gamma", "Delta", "All Positions"],
                2,  # 2 columns for positions
            ),
            # Author-based filters (dynamic based on available data)
            (
                "👤 By Author",
                FilterType.AUTHOR,
                self._get_available_authors(),
                2,  # 2 columns for authors
            ),
            # Grid mode filters
            (
                "🎨 By Grid Style",
                FilterType.GRID_MODE,
                [
                    ("💎 Diamond Grid", "diamond"),
                    ("⬜ Box Grid", "box"),
                    ("All Styles", "all"),
                ],
                3,  # 3 columns for grid styles
            ),
        ]

        # Create and add category sections
        self.category_sections = {}
        for i, (title, filter_type, options, columns) in enumerate(categories):
            section = FilterCategorySection(title, filter_type, options, columns)
            self.category_sections[filter_type] = section

            # Add to grid layout (2 columns of categories)
            row = i // self._category_columns
            col = i % self._category_columns
            self.categories_layout.addWidget(section, row, col)

    def _get_available_authors(self) -> list:
        """Get available authors from the dictionary manager."""
        try:
            authors = self.dictionary_manager.get_distinct_authors()
            # Limit to top authors + "All"
            result = authors[:4] if len(authors) > 4 else authors
            result.append("All Authors")
            return result
        except Exception as e:
            print(f"Error getting authors: {e}")
            return ["Demo Author", "Test User", "All Authors"]

    def _connect_signals(self) -> None:
        """Connect component signals."""
        # Quick access signals
        self.quick_access.filter_selected.connect(self._handle_filter_selection)

        # Category section signals
        for section in self.category_sections.values():
            section.filter_selected.connect(self._handle_filter_selection)

    def _handle_filter_selection(self, filter_type: FilterType, filter_value) -> None:
        """Handle filter selection from any component."""
        print(
            f"🔍 [FILTER PANEL] Filter selected: {filter_type.value} = {filter_value}"
        )
        self.filter_selected.emit(filter_type, filter_value)

    def _apply_container_styling(self) -> None:
        """Apply modern container styling using the design system."""
        # Apply panel styling to the main container
        self.apply_panel_style(StyleVariant.SUBTLE)

    def _finalize_layout_initialization(self) -> None:
        """Finalize layout initialization after widget is shown."""
        self._layout_initialized = True
        self._update_responsive_layout()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events for responsive layout."""
        super().resizeEvent(event)
        if self._layout_initialized:
            self._update_responsive_layout()

    def _update_responsive_layout(self) -> None:
        """Update layout based on current widget size."""
        if not self.isVisible() or self.width() < 100:
            return

        # Calculate optimal category columns based on width
        widget_width = self.width()

        if widget_width < 800:
            new_columns = 1  # Stack categories vertically on narrow screens
        elif widget_width < 1200:
            new_columns = 2  # Standard 2-column layout
        else:
            new_columns = 3  # Wide 3-column layout for large screens

        # Update layout if column count changed
        if new_columns != self._category_columns:
            self._category_columns = new_columns
            self._reorganize_categories()

    def _reorganize_categories(self) -> None:
        """Reorganize category sections with new column count."""
        # Remove all sections from layout
        sections = []
        for i in range(self.categories_layout.count()):
            item = self.categories_layout.itemAt(i)
            if item and item.widget():
                sections.append(item.widget())

        # Clear layout
        for i in range(self.categories_layout.count()):
            self.categories_layout.takeAt(0)

        # Re-add sections with new column count
        for i, section in enumerate(sections):
            if section:
                row = i // self._category_columns
                col = i % self._category_columns
                self.categories_layout.addWidget(section, row, col)

    def set_active_filter(
        self, filter_type: FilterType | None, filter_value=None
    ) -> None:
        """Highlight the active filter across all sections."""
        # Update quick access
        self.quick_access.set_active_filter(filter_type)

        # Update category sections
        for section_filter_type, section in self.category_sections.items():
            if section_filter_type == filter_type:
                section.set_active_option(filter_value)
            else:
                section.set_active_option(None)
