"""
Section Layout Manager - Qt Presentation Layer

Handles Qt-specific layout operations while delegating calculations
to SectionLayoutService.
"""

from typing import Optional

from application.services.option_picker.section_layout_manager import (
    LayoutDimensions,
    SectionLayoutManager,
    SizingConstraints,
)
from presentation.components.option_picker.components.sections.section_widget import (
    OptionPickerSection,
)
from presentation.components.option_picker.types.letter_types import LetterType


class SectionLayoutManager:
    """
    Qt presentation manager for section layout.

    Handles Qt-specific operations while delegating calculations
    to SectionLayoutService.
    """

    def __init__(
        self,
        section_widget: "OptionPickerSection",
        layout_service: SectionLayoutManager,
    ):
        self.section = section_widget
        self._layout_service = layout_service
        self._last_width = None
        self._resize_in_progress = False
        self._debug_logged = False
        self._option_picker_width = 0
        self._sizing_deferred = False
        self._current_dimensions: Optional[LayoutDimensions] = None

    def defer_sizing_updates(self):
        """Defer sizing updates for batch operations."""
        self._sizing_deferred = True

    def resume_sizing_updates(self):
        """Resume sizing updates."""
        self._sizing_deferred = False

    def update_size_once(self):
        """Force a single size update."""
        self._update_size()

    def add_pictograph_from_pool(self, pictograph_frame):
        """Add pictograph and update layout if not deferred."""
        if not self._sizing_deferred:
            self._ensure_container_ready()

        self.section.section_pictograph_container.sync_width_with_section()
        self.section.section_pictograph_container.add_pictograph(pictograph_frame)

        if not self._sizing_deferred:
            self._update_size()

    def _update_size(self):
        """Update section size using the layout service."""
        try:
            # Prepare constraints
            constraints = self._create_sizing_constraints()

            # Get header height
            header_height = self.section.header.get_calculated_height()

            # Calculate dimensions using service
            dimensions = self._layout_service.calculate_section_height(
                constraints, header_height
            )

            # Validate dimensions
            if not self._layout_service.validate_dimensions(dimensions):
                print(f"⚠️ Invalid dimensions calculated for {self.section.letter_type}")
                return

            # Apply dimensions to Qt widgets
            self._apply_dimensions_to_widgets(dimensions)

            # Cache dimensions
            self._current_dimensions = dimensions
            self._layout_service.cache_dimensions(constraints, dimensions)

        except Exception as e:
            print(f"⚠️ [ERROR] Size update failed for {self.section.letter_type}: {e}")

    def _create_sizing_constraints(self) -> SizingConstraints:
        """Create sizing constraints from current widget state."""
        # Get main window width
        main_window_width = (
            self.section.option_picker_size_provider().width()
            if self.section.option_picker_size_provider
            else 800  # Default fallback
        )

        # Get container width
        container_width = (
            self.section.section_pictograph_container.width()
            if self.section.section_pictograph_container.width() > 0
            else self.section.width()
        )

        if container_width <= 0:
            container_width = main_window_width

        # Get spacing from layout
        spacing = (
            self.section.section_pictograph_container.main_layout.spacing()
            if hasattr(self.section.section_pictograph_container, "main_layout")
            else 8  # Default
        )

        return SizingConstraints(
            main_window_width=main_window_width,
            container_width=container_width,
            letter_type=self.section.letter_type,
            spacing=spacing,
        )

    def _apply_dimensions_to_widgets(self, dimensions: LayoutDimensions):
        """Apply calculated dimensions to Qt widgets."""
        # Sync container width
        self.section.section_pictograph_container.sync_width_with_section()

        # Resize pictographs using service-calculated size
        self.section.section_pictograph_container.resize_pictographs(
            dimensions.pictograph_size
        )

        # Set section height
        self.section.setMinimumHeight(dimensions.section_height)
        self.section.resize(self.section.width(), dimensions.section_height)

        # Update header if needed
        self._update_header_with_dimensions(dimensions)

        # Trigger Qt layout updates
        self.section.updateGeometry()
        if self.section.parent():
            self.section.parent().updateGeometry()

    def _update_header_with_dimensions(self, dimensions: LayoutDimensions):
        """Update header sizing based on calculated dimensions."""
        if hasattr(self.section.header, "type_button"):
            self.section.header.type_button._resizing = True
            try:
                self.section.header.setFixedHeight(dimensions.header_height)

                # Calculate button size if provider available
                if (
                    hasattr(self.section, "option_picker_size_provider")
                    and self.section.option_picker_size_provider
                ):
                    parent_height = self.section.option_picker_size_provider().height()
                    font_size = max(parent_height // 70, 10)
                    label_height = max(int(font_size * 3), 20)
                    label_width = max(int(label_height * 6), 100)

                    from PyQt6.QtCore import QSize

                    self.section.header.type_button.setFixedSize(
                        QSize(label_width, label_height)
                    )
            finally:
                self.section.header.type_button._resizing = False

    def handle_resize_event(self, event):
        """Handle resize events using the layout service."""
        if self._resize_in_progress:
            return

        self._resize_in_progress = True
        try:
            # Get new width from service calculation
            if self.section.option_picker_size_provider:
                full_width = self.section.option_picker_size_provider().width()
                new_width = self._layout_service.calculate_section_width(
                    self.section.letter_type, full_width
                )

                # Check if resize is significant using service
                if self._current_dimensions and self._last_width is not None:
                    new_dimensions = self._layout_service.calculate_resize_dimensions(
                        self._last_width, new_width, self._current_dimensions
                    )

                    if new_dimensions:
                        self._apply_dimensions_to_widgets(new_dimensions)
                        self._current_dimensions = new_dimensions

                self._last_width = new_width
                self.section.setFixedWidth(new_width)
                self.section.section_pictograph_container.sync_width_with_section()

        except Exception as e:
            print(f"⚠️ [ERROR] Resize failed for {self.section.letter_type}: {e}")
        finally:
            self._resize_in_progress = False

    def register_for_sizing_updates(self):
        """Register this section to receive sizing updates."""
        widget = self.section.parent()
        while widget:
            if (
                hasattr(widget, "__class__")
                and "OptionPickerWidget" in widget.__class__.__name__
            ):
                widget.add_sizing_callback(self._on_option_picker_resize)
                # Removed repetitive log statement
                break
            widget = widget.parent()

    def _on_option_picker_resize(self, option_picker_width: int):
        """Handle option picker width changes."""
        self._option_picker_width = option_picker_width
        if hasattr(self.section, "section_pictograph_container"):
            self.section.section_pictograph_container.update_sizing_reference(
                option_picker_width
            )

    def _ensure_container_ready(self):
        """Ensure container is ready without forced event processing."""
        if self.section.parent():
            widget = self.section.parent()
            while widget:
                if (
                    hasattr(widget, "__class__")
                    and "ModernOptionPickerWidget" in widget.__class__.__name__
                ):
                    widget.updateGeometry()
                    break
                elif (
                    hasattr(widget, "layout")
                    and widget.layout()
                    and widget.layout().__class__.__name__ == "QVBoxLayout"
                    and widget.width() > 500
                ):
                    widget.updateGeometry()
                    break
                widget = widget.parent()

    # State Access
    def get_current_dimensions(self) -> Optional[LayoutDimensions]:
        """Get current layout dimensions."""
        return self._current_dimensions

    def get_layout_summary(self) -> dict:
        """Get layout summary for debugging."""
        if self._current_dimensions:
            return self._layout_service.get_layout_summary(self._current_dimensions)
        return {"status": "no_dimensions"}
