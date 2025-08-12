"""
Text Overlay Base Component for Modern Beat Views

This base class provides common functionality for text overlays that display
on beat views and start position views, using the reliable widget overlay
approach that provides consistent visibility and natural scene integration.

Unified approach based on successful BeatNumberOverlay implementation.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QWidget


class TextOverlayBase(QLabel):
    """
    Base class for text overlay widgets that display text on beat/start position views.

    Uses transparent widget overlay approach for reliable visibility
    and natural integration with the view appearance.

    Provides common scaling, positioning, and styling functionality.
    """

    def __init__(self, text: str, parent_widget: QWidget | None = None):
        super().__init__(text, parent_widget)

        self._parent_widget = parent_widget
        self._base_font_size = 10  # Base font size for scaling
        self._base_size = (25, 25)  # Base size for scaling (can be overridden)
        self._base_position = (
            5,
            2,
        )  # Base position for scaling - moved left to prevent cutoff

        # Hover scaling state
        self._hover_scale_factor = 1.0
        self._is_hover_scaled = False

        self._setup_styling()
        self._setup_positioning()

        # Initially hidden until explicitly shown
        self.hide()

    def _setup_styling(self):
        """Setup the text styling to match Legacy's appearance exactly"""
        # Use the exact settings determined from successful testing
        self.setFont(QFont("Georgia", 10, QFont.Weight.DemiBold))

        # Transparent styling for natural scene integration
        self.setStyleSheet(
            """
            QLabel {
                color: black;
                background: transparent;
                border: none;
                padding: 0px;
            }
        """
        )

        # Ensure text alignment
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def _setup_positioning(self):
        """Setup the positioning and sizing based on successful test results"""
        # Use the base dimensions - subclasses can override _base_size
        self.setGeometry(
            self._base_position[0],
            self._base_position[1],
            self._base_size[0],
            self._base_size[1],
        )

    def show_overlay(self):
        """Show the text overlay - implemented by subclasses"""
        self._show_overlay_common()

    def hide_overlay(self):
        """Hide the text overlay - implemented by subclasses"""
        self._hide_overlay_common()

    def update_text(self, new_text: str):
        """Update the displayed text"""
        self.setText(new_text)

    def update_position(self, x: int, y: int):
        """Update the overlay position"""
        current_geometry = self.geometry()
        self.setGeometry(x, y, current_geometry.width(), current_geometry.height())

    def update_size(self, width: int, height: int):
        """Update the overlay size"""
        current_geometry = self.geometry()
        self.setGeometry(current_geometry.x(), current_geometry.y(), width, height)

    def update_scaling(self, additional_scale_factor: float = 1.0):
        """Update the overlay scaling based on parent widget size and hover state"""
        if not self._parent_widget:
            return

        # Safety check: ensure the Qt object is still valid
        try:
            # Test if we can access Qt properties without crashing
            _ = self.isVisible()
            _ = self.geometry()
        except (RuntimeError, AttributeError):
            # Qt object has been deleted, skip scaling
            return

        # Calculate scale factor based on parent widget size vs base size (120x120)
        parent_size = self._parent_widget.size()
        base_size = 120  # Base size that the original overlay was designed for

        base_scale_factor = min(
            parent_size.width() / base_size, parent_size.height() / base_size
        )

        # Apply additional scaling (for hover effects)
        total_scale_factor = (
            base_scale_factor * additional_scale_factor * self._hover_scale_factor
        )

        try:
            # Scale font size with safety check
            scaled_font_size = max(
                6, int(self._base_font_size * total_scale_factor)
            )  # Minimum 6pt
            current_font = self.font()
            current_font.setPointSize(scaled_font_size)
            self.setFont(current_font)

            # Calculate center-based scaling transformation to match pictograph scene
            if self._is_hover_scaled:
                # Apply center-based scaling transformation like pictograph scene
                scaled_x, scaled_y, scaled_width, scaled_height = (
                    self._calculate_center_based_scaling(total_scale_factor)
                )
            else:
                # Normal scaling from top-left
                scaled_x = int(self._base_position[0] * total_scale_factor)
                scaled_y = int(self._base_position[1] * total_scale_factor)
                scaled_width = int(self._base_size[0] * total_scale_factor)
                scaled_height = int(self._base_size[1] * total_scale_factor)

            self.setGeometry(scaled_x, scaled_y, scaled_width, scaled_height)

        except (RuntimeError, AttributeError):
            # Qt object was deleted during scaling, ignore
            pass

    def _calculate_center_based_scaling(
        self, total_scale_factor: float
    ) -> tuple[int, int, int, int]:
        """
        Calculate center-based scaling transformation to match pictograph scene behavior.

        This ensures text overlays scale toward the center of the parent widget,
        matching the pictograph scene's center-based scaling during hover effects.
        """
        if not self._parent_widget:
            return (0, 0, 0, 0)

        # Get parent widget center point
        parent_size = self._parent_widget.size()
        parent_center_x = parent_size.width() / 2
        parent_center_y = parent_size.height() / 2

        # Calculate normal scaled dimensions
        normal_scaled_width = int(self._base_size[0] * total_scale_factor)
        normal_scaled_height = int(self._base_size[1] * total_scale_factor)
        normal_scaled_x = int(self._base_position[0] * total_scale_factor)
        normal_scaled_y = int(self._base_position[1] * total_scale_factor)

        # Calculate the center of the normally scaled overlay
        overlay_center_x = normal_scaled_x + normal_scaled_width / 2
        overlay_center_y = normal_scaled_y + normal_scaled_height / 2

        # Calculate the vector from parent center to overlay center
        offset_x = overlay_center_x - parent_center_x
        offset_y = overlay_center_y - parent_center_y

        # Apply hover scale factor to the offset (this creates center-based scaling)
        scaled_offset_x = offset_x * self._hover_scale_factor
        scaled_offset_y = offset_y * self._hover_scale_factor

        # Calculate new overlay center position
        new_overlay_center_x = parent_center_x + scaled_offset_x
        new_overlay_center_y = parent_center_y + scaled_offset_y

        # Calculate new overlay dimensions (also scaled by hover factor)
        new_overlay_width = int(normal_scaled_width * self._hover_scale_factor)
        new_overlay_height = int(normal_scaled_height * self._hover_scale_factor)

        # Calculate new top-left position from center
        new_x = int(new_overlay_center_x - new_overlay_width / 2)
        new_y = int(new_overlay_center_y - new_overlay_height / 2)

        return (new_x, new_y, new_overlay_width, new_overlay_height)

    def set_hover_scale(self, scale_factor: float):
        """Set hover scale factor and update display"""
        try:
            # Safety check: ensure the Qt object is still valid
            _ = self.isVisible()
            self._hover_scale_factor = scale_factor
            self._is_hover_scaled = scale_factor != 1.0
            self.update_scaling()
        except (RuntimeError, AttributeError):
            # Qt object has been deleted, skip scaling
            pass

    def apply_hover_scaling(self, scale_factor: float = 0.95):
        """Apply hover scaling to match pictograph shrinking effect"""
        try:
            self.set_hover_scale(scale_factor)
        except (RuntimeError, AttributeError):
            # Qt object has been deleted, skip scaling
            pass

    def remove_hover_scaling(self):
        """Remove hover scaling to return to normal size"""
        try:
            self.set_hover_scale(1.0)
        except (RuntimeError, AttributeError):
            # Qt object has been deleted, skip scaling
            pass

    def update_font_size(self, font_size: int):
        """Update the font size"""
        current_font = self.font()
        current_font.setPointSize(font_size)
        self.setFont(current_font)

    def _show_overlay_common(self):
        """Common show logic for all overlays"""
        self.show()
        self.raise_()  # Bring to front to ensure visibility
        # Ensure proper scaling when first shown
        self.update_scaling()

    def _hide_overlay_common(self):
        """Common hide logic for all overlays"""
        self.hide()


def add_text_overlay_to_view(
    view_widget: QWidget, overlay_instance
) -> object | None:
    """
    Add text overlay to a view widget with proper lifecycle management.

    Args:
        view_widget: View widget instance (BeatView, StartPositionView, etc.)
        overlay_instance: TextOverlayBase instance to add

    Returns:
        The overlay instance if successful, None otherwise
    """
    if not view_widget or not overlay_instance:
        return None

    try:
        # Show the overlay
        overlay_instance.show_overlay()

        # Store reference on the view widget to prevent garbage collection
        if not hasattr(view_widget, "_text_overlays"):
            view_widget._text_overlays = []
        view_widget._text_overlays.append(overlay_instance)

        return overlay_instance

    except Exception as e:
        print(f"Failed to add text overlay: {e}")
        return None


def remove_text_overlay_from_view(view_widget: QWidget, overlay_instance):
    """
    Remove text overlay from a view widget.

    Args:
        view_widget: View widget instance
        overlay_instance: TextOverlayBase instance to remove
    """
    if not overlay_instance:
        return

    try:
        # Remove from view widget's overlay list
        if (
            hasattr(view_widget, "_text_overlays")
            and overlay_instance in view_widget._text_overlays
        ):
            view_widget._text_overlays.remove(overlay_instance)

        # Hide and delete the overlay
        overlay_instance.hide_overlay()
        overlay_instance.deleteLater()

    except Exception as e:
        print(f"Failed to remove text overlay: {e}")
