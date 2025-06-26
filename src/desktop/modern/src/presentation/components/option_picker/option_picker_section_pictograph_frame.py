from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .option_picker_section import OptionPickerSection


class OptionPickerSectionPictographFrame(QFrame):
    """
    Frame widget for holding pictographs in a grid layout.
    Handles pictograph-specific layout and sizing.
    """

    def __init__(self, section: "OptionPickerSection"):
        super().__init__()
        self.section = section
        self.pictographs = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup grid layout for pictographs exactly like legacy system."""
        self.layout = QGridLayout(self)
        # CRITICAL: Use center alignment like original legacy system
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(3)  # CRITICAL: Use original spacing value (3, not 8)

        # Make sure the frame expands to fill available width
        from PyQt6.QtWidgets import QSizePolicy

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Ensure frame width matches section width exactly
        self.setMinimumWidth(0)  # Allow shrinking
        self.setMaximumWidth(16777215)  # Allow expanding (Qt max)

        # Set transparent background
        self.setStyleSheet(
            """
            QFrame {
                background-color: transparent;
                border: none;
            }
            """
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def add_pictograph(self, pictograph_frame):
        """Add pictograph to grid layout."""
        self.pictographs.append(pictograph_frame)

        # Set container widget for legacy-style resizing
        if hasattr(pictograph_frame, "set_container_widget"):
            pictograph_frame.set_container_widget(self.section)

        # Use 8-column layout like legacy for top sections (Types 1,2,3)
        COLUMN_COUNT = 8
        count = len(self.pictographs)
        row, col = divmod(count - 1, COLUMN_COUNT)

        self.layout.addWidget(pictograph_frame, row, col)
        pictograph_frame.setVisible(True)

    def clear_pictographs(self):
        """Clear all pictographs from the frame."""
        for pictograph in self.pictographs:
            if pictograph is not None:
                try:
                    if hasattr(pictograph, "cleanup"):
                        pictograph.cleanup()
                    self.layout.removeWidget(pictograph)
                    pictograph.setParent(None)
                    pictograph.deleteLater()
                except RuntimeError:
                    pass
        self.pictographs.clear()

    def clear_pictographs_pool_style(self):
        """Clear pictographs using pool approach (don't delete, just hide)."""
        for pictograph in self.pictographs:
            if pictograph is not None:
                try:
                    self.layout.removeWidget(pictograph)
                    pictograph.setVisible(False)
                except RuntimeError:
                    pass
        self.pictographs.clear()

    def add_pictograph_from_pool(self, pictograph_frame):
        """Add pictograph from pool."""
        self.pictographs.append(pictograph_frame)

        # Set container widget for legacy-style resizing
        if hasattr(pictograph_frame, "set_container_widget"):
            pictograph_frame.set_container_widget(self.section)

        # Use 8-column layout like legacy
        COLUMN_COUNT = 8
        count = len(self.pictographs)
        row, col = divmod(count - 1, COLUMN_COUNT)

        self.layout.addWidget(pictograph_frame, row, col)
        pictograph_frame.setVisible(True)
        pictograph_frame.show()

        if hasattr(pictograph_frame, "pictograph_component"):
            pictograph_frame.pictograph_component.setVisible(True)
            pictograph_frame.pictograph_component.show()

    def resize_pictographs(self, target_size: int):
        """Resize all pictographs using legacy algorithm."""
        for pictograph_frame in self.pictographs:
            if pictograph_frame and hasattr(pictograph_frame, "resize_frame"):
                try:
                    # Use the frame's own resize_frame method which implements legacy algorithm
                    pictograph_frame.resize_frame()
                except RuntimeError:
                    continue
            elif pictograph_frame and hasattr(pictograph_frame, "setFixedSize"):
                try:
                    # Fallback for frames without resize_frame method
                    pictograph_frame.setFixedSize(target_size, target_size)
                except RuntimeError:
                    continue

    def calculate_required_height(self, pictograph_size: int) -> int:
        """Calculate the height required for current pictographs."""
        if len(self.pictographs) == 0:
            return 0

        COLUMN_COUNT = 8
        max_row = (len(self.pictographs) - 1) // COLUMN_COUNT
        rows_needed = max_row + 1

        container_margins = 0  # Frame has no margins
        grid_spacing = 8

        return (
            (rows_needed * pictograph_size)
            + (grid_spacing * (rows_needed - 1))
            + (2 * container_margins)
        )
