from typing import TYPE_CHECKING

from presentation.components.option_picker.components.frames.pictograph_option_frame import (
    PictographOptionFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QGridLayout

if TYPE_CHECKING:
    from presentation.components.option_picker.components.sections.section_widget import (
        OptionPickerSection,
    )


class OptionPickerSectionPictographContainer(QFrame):
    """
    Frame widget for holding pictographs in a grid layout.
    Handles pictograph-specific layout and sizing.
    """

    def __init__(self, section: "OptionPickerSection"):
        super().__init__()
        self.section = section
        self.pictographs: list[QFrame] = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup grid layout for pictographs exactly like legacy system."""
        self.main_layout = QGridLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(3)

        from PyQt6.QtWidgets import QSizePolicy

        # Allow sections to size based on content height (like legacy)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.setStyleSheet(
            """
            QFrame {
                background-color: transparent;
                border: none;
            }
            """
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def sync_width_with_section(self):
        """Ensure frame width exactly matches section width."""
        if self.section and self.section.width() > 0:
            self.setFixedWidth(self.section.width())

    def clear_pictographs(self):
        """Clear all pictographs from the frame."""
        for pictograph in self.pictographs:
            if pictograph is not None:
                try:
                    if hasattr(pictograph, "cleanup"):
                        pictograph.cleanup()
                    self.main_layout.removeWidget(pictograph)
                    pictograph.setParent(None)
                    pictograph.deleteLater()
                except RuntimeError:
                    pass
        self.pictographs.clear()

    def remove_pictographs_for_reuse(self):
        """Remove pictographs from container without destroying them (for pool reuse)."""
        for pictograph in self.pictographs:
            if pictograph is not None:
                try:
                    # Remove from layout but DON'T call cleanup() or deleteLater()
                    # so the frames can be reused by the pool
                    self.main_layout.removeWidget(pictograph)
                    pictograph.setParent(None)
                    pictograph.setVisible(False)
                except RuntimeError:
                    pass
        self.pictographs.clear()

    def clear_pictographs_pool_style(self):
        """Clear pictographs using pool approach (don't delete, just hide)."""
        for pictograph in self.pictographs:
            if pictograph is not None:
                try:
                    self.main_layout.removeWidget(pictograph)
                    pictograph.setVisible(False)
                except RuntimeError:
                    pass
        self.pictographs.clear()

    def add_pictograph(self, pictograph_frame: "PictographOptionFrame"):
        """Add pictograph from pool."""
        import logging

        logger = logging.getLogger(__name__)

        # Debug: Check frame state at the very start of add_pictograph
        has_component_start = (
            hasattr(pictograph_frame, "pictograph_component")
            and pictograph_frame.pictograph_component
        )
        logger.debug(
            f"🎯 add_pictograph called: Frame {id(pictograph_frame)} has_component={has_component_start}"
        )

        self.pictographs.append(pictograph_frame)
        logger.debug(
            f"   📝 After append: has_component={hasattr(pictograph_frame, 'pictograph_component') and pictograph_frame.pictograph_component}"
        )

        if hasattr(pictograph_frame, "set_container_widget"):
            pictograph_frame.set_container_widget(self.section)
            logger.debug(
                f"   🏠 After set_container_widget: has_component={hasattr(pictograph_frame, 'pictograph_component') and pictograph_frame.pictograph_component}"
            )

        COLUMN_COUNT = 8
        count = len(self.pictographs)
        row, col = divmod(count - 1, COLUMN_COUNT)

        self.main_layout.addWidget(pictograph_frame, row, col)
        pictograph_frame.setVisible(True)
        pictograph_frame.show()

        if (
            hasattr(pictograph_frame, "pictograph_component")
            and pictograph_frame.pictograph_component
        ):
            pictograph_frame.pictograph_component.setVisible(True)
            pictograph_frame.pictograph_component.show()
        else:
            # Debug: Log when pictograph_component is missing
            logger.warning(
                f"Frame {id(pictograph_frame)} has no pictograph_component or it's None"
            )

    def resize_pictographs(self, target_size: int):
        """Resize all pictographs using legacy algorithm."""
        # Only print summary, not per-pictograph logs

        for pictograph_frame in self.pictographs:
            if pictograph_frame and hasattr(pictograph_frame, "resize_frame"):
                try:
                    pictograph_frame.resize_frame()
                except RuntimeError:
                    continue
            elif pictograph_frame and hasattr(pictograph_frame, "setFixedSize"):
                try:
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

        container_margins = 0
        grid_spacing = self.main_layout.spacing()

        return (
            (rows_needed * pictograph_size)
            + (grid_spacing * (rows_needed - 1))
            + (2 * container_margins)
        )

    def update_sizing_reference(self, option_picker_width: int):
        """Update sizing reference for all pictograph frames in this container"""
        # Removed repetitive log statement

        for pictograph_frame in self.pictographs:
            if pictograph_frame and hasattr(
                pictograph_frame, "update_sizing_reference"
            ):
                pictograph_frame.update_sizing_reference(option_picker_width)
