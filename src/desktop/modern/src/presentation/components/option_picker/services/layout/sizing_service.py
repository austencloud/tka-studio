"""
Responsive Sizing Service - Dynamic Sizing Management
Split from responsive_sizing_manager.py - contains core sizing coordination
"""

from typing import Dict, Callable, Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QSize, QTimer, pyqtSignal, QObject


class ResponsiveSizingService(QObject):
    """
    Dynamic sizing service that ensures option picker never requires scrolling.
    Coordinates sizing across all components.
    """

    sizing_changed = pyqtSignal()

    def __init__(
        self,
        option_picker_widget: QWidget,
        sections_container: QWidget,
        filter_widget: Optional[QWidget] = None,
    ):
        super().__init__()
        self.option_picker_widget = option_picker_widget
        self.sections_container = sections_container
        self.filter_widget = filter_widget

        # Initialize dimension calculator
        from presentation.components.option_picker.services.layout.dimension_calculator import (
            DimensionCalculator,
        )

        self.dimension_calculator = DimensionCalculator()

        # Sizing parameters
        self.sections: Dict[str, QWidget] = {}
        self.section_headers: Dict[str, QWidget] = {}
        self._current_sizing: Optional[Dict] = None

        # Resize timer for performance
        self.resize_timer = QTimer()
        self.resize_timer.timeout.connect(self._recalculate_sizing)
        self.resize_timer.setSingleShot(True)

    def register_section(
        self, section_type: str, section_widget: QWidget, header_widget: QWidget
    ):
        """Register a section for dynamic sizing management."""
        self.sections[section_type] = section_widget
        self.section_headers[section_type] = header_widget
        original_resize = section_widget.resizeEvent
        section_widget.resizeEvent = self._create_resize_handler(original_resize)

    def calculate_dynamic_sizing(self) -> Dict:
        """Calculate comprehensive sizing for all elements."""
        optimal_size = self.dimension_calculator.calculate_optimal_size(
            self.option_picker_widget
        )
        container_width = optimal_size.width()
        container_height = optimal_size.height()

        section_count = len(self.sections) if self.sections else 6
        filter_height = 40 if self.filter_widget else 0

        sizing_config = self.dimension_calculator.calculate_component_sizing(
            container_width, container_height, section_count, filter_height
        )

        self._current_sizing = sizing_config
        return sizing_config

    def apply_sizing_to_sections(self):
        """Apply calculated sizing to all registered sections."""
        if not self._current_sizing:
            self.calculate_dynamic_sizing()

        sizing = self._current_sizing
        if not sizing:
            return

        for section_type, section_widget in self.sections.items():
            self._apply_section_sizing(section_widget, section_type, sizing)

        for section_type, header_widget in self.section_headers.items():
            self._apply_header_sizing(header_widget, sizing)

        self.sizing_changed.emit()

    def _apply_section_sizing(
        self, section_widget: QWidget, section_type: str, sizing: Dict
    ):
        """Apply sizing to individual section."""
        if section_type in ["Type1", "Type2", "Type3"]:
            width = sizing["individual_section_width"]
        else:
            width = sizing["shared_section_width"]

        section_widget.setFixedWidth(width)
        max_section_height = (
            sizing["header_height"]
            + sizing["pictograph_space_per_section"]
            + sizing["section_margins"] * 2
        )
        section_widget.setMaximumHeight(max_section_height)

    def _apply_header_sizing(self, header_widget: QWidget, sizing: Dict):
        """Apply dynamic sizing to section header."""
        if hasattr(header_widget, "setFixedHeight"):
            header_widget.setFixedHeight(sizing["header_height"])

        if hasattr(header_widget, "set_dynamic_sizing"):
            header_widget.set_dynamic_sizing(sizing)

    def get_dynamic_size_provider(self) -> Callable[[], QSize]:
        """Returns a size provider for optimal dimensions."""

        def size_provider():
            if self._current_sizing:
                return QSize(
                    self._current_sizing["container_width"],
                    self._current_sizing["container_height"],
                )
            return self.dimension_calculator.calculate_optimal_size(
                self.option_picker_widget
            )

        return size_provider

    def schedule_resize_recalculation(self):
        """Schedule a resize recalculation (debounced for performance)."""
        self.resize_timer.start(100)

    def _recalculate_sizing(self):
        """Recalculate and apply sizing after resize."""
        self.calculate_dynamic_sizing()
        self.apply_sizing_to_sections()

    def _create_resize_handler(self, original_resize_event):
        """Create a resize event handler that triggers recalculation."""

        def new_resize_event(event):
            original_resize_event(event)
            self.schedule_resize_recalculation()

        return new_resize_event

    def get_sizing_info(self) -> Dict:
        """Get current sizing information for debugging."""
        if not self._current_sizing:
            self.calculate_dynamic_sizing()
        return self._current_sizing.copy() if self._current_sizing else {}

    def set_sizing_constraints(
        self,
        min_header: Optional[int] = None,
        max_header: Optional[int] = None,
        min_pictograph: Optional[int] = None,
        max_pictograph: Optional[int] = None,
    ):
        """Update sizing constraints and recalculate."""
        if min_header is not None:
            self.dimension_calculator.min_header_height = min_header
        if max_header is not None:
            self.dimension_calculator.max_header_height = max_header
        if min_pictograph is not None:
            self.dimension_calculator.min_pictograph_size = min_pictograph
        if max_pictograph is not None:
            self.dimension_calculator.max_pictograph_size = max_pictograph

        self.schedule_resize_recalculation()
