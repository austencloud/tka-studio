"""
Start Position View Component

Displays the start position in the sequence workbench beat frame,
integrating with Modern's start position picker and pictograph system.
"""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from desktop.modern.domain.models import BeatData
from desktop.modern.domain.models.pictograph_data import PictographData

from .selection_overlay import SelectionOverlay
from .start_text_overlay import StartTextOverlay, add_start_text_to_view
from ...pictograph.views import create_beat_view
from ...pictograph.views.beat_pictograph_view import BeatPictographView


class StartPositionView(QFrame):
    """
    Start position display widget for the sequence workbench.

    Shows the initial position of a sequence with pictograph rendering
    and integrates with the Modern start position picker workflow.
    """

    # Additional signals specific to start position
    start_pos_beat_clicked = pyqtSignal()
    start_pos_beat_context_menu = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        print(
            f"🔧 [START_POS_VIEW] Initializing StartPositionView with parent: {parent}"
        )

        # Common state (previously from PictographViewBase)
        self._beat_data: Optional[BeatData] = None
        self._pictograph_data: Optional[PictographData] = (
            None  # NEW: Separate pictograph data
        )
        self._is_selected = False
        self._is_highlighted = False

        # UI components
        self._pictograph_component: Optional[BeatPictographView] = None
        self._selection_overlay: Optional[SelectionOverlay] = None

        # Additional state specific to start position
        self._position_key: Optional[str] = None
        self._start_text_overlay: Optional[StartTextOverlay] = None
        self._text_overlays = []  # Initialize text overlays list

        # Initialize UI
        self._setup_ui()
        self._setup_styling()
        self._create_selection_overlay()

    def _setup_ui(self):
        """Setup the UI structure"""
        self.setFixedSize(120, 120)
        self.setFrameStyle(QFrame.Shape.Box)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create direct pictograph view for start position in beat frame (no widget wrapper)
        self._pictograph_component = create_beat_view(parent=self)

        # Ensure pictograph component is visible (needed for blank white background)
        self._pictograph_component.show()
        self._pictograph_component.setVisible(True)

        layout.addWidget(self._pictograph_component)

        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)

    def _setup_styling(self):
        """Setup clean base styling"""
        self.setStyleSheet(
            """
            QFrame {
                background: transparent;
                border: none;
            }
            QFrame:hover {
                background: rgba(255, 255, 255, 0.05);
            }
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                border: none;
            }
        """
        )
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def _create_selection_overlay(self):
        """Create the selection overlay widget"""
        self._selection_overlay = SelectionOverlay(self)
        self._selection_overlay.hide()

    def _update_display(self):
        """Update the pictograph display - delegates to the new separate data approach"""
        self._update_pictograph()

    # Direct view handles its own scaling and styling - no configuration needed
    # State management
    def set_beat_data(self, beat_data: Optional[BeatData]):
        """Set beat data and update display"""
        if self._beat_data != beat_data:
            self._beat_data = beat_data
            self._update_display()

    def set_pictograph_data(self, pictograph_data: Optional[PictographData]):
        """Set pictograph data for direct rendering (separate approach)"""
        if self._pictograph_data != pictograph_data:
            self._pictograph_data = pictograph_data
            self._update_display()

    def set_selected(self, selected: bool):
        """Set selection state"""
        if self._is_selected != selected:
            self._is_selected = selected
            self._update_cursor()

            # Show/hide selection overlay
            if selected:
                self._selection_overlay.show_selection()
            else:
                self._selection_overlay.hide_selection()

    def is_selected(self) -> bool:
        """Check if view is selected"""
        return self._is_selected

    def set_position_data(
        self, beat_data: BeatData, pictograph_data: Optional[PictographData] = None
    ):
        """
        Set the start position data and update display.

        Args:
            beat_data: Beat context data (beat number, duration, metadata)
            pictograph_data: Optional pictograph data for direct rendering.
                           If None, will be reconstructed from beat_data (legacy mode)
        """
        self.set_beat_data(beat_data)
        if pictograph_data is not None:
            self.set_pictograph_data(pictograph_data)
        else:
            # Legacy mode: clear pictograph data to force reconstruction
            self._pictograph_data = None

    def _add_start_text_overlay(self):
        """Add START text overlay using the unified widget approach"""
        self._cleanup_existing_overlay()

        try:
            self._start_text_overlay = add_start_text_to_view(self)
            if self._start_text_overlay:
                self._text_overlays = [self._start_text_overlay]
        except Exception as e:
            print(f"Failed to create start text overlay: {e}")
            self._start_text_overlay = None

    def _cleanup_existing_overlay(self):
        """Safely cleanup existing overlay"""
        if not self._start_text_overlay:
            return

        try:
            self._start_text_overlay.hide_overlay()
            self._start_text_overlay.deleteLater()
        except Exception as e:
            print(f"Error cleaning up start text overlay: {e}")
        finally:
            self._start_text_overlay = None
            if hasattr(self, "_text_overlays"):
                self._text_overlays.clear()

    # Override mouse press to emit specific signals
    def mousePressEvent(self, event):
        """Handle mouse press events"""
        from PyQt6.QtCore import Qt

        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos_beat_clicked.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.start_pos_beat_context_menu.emit()

        # Also emit the base class signal
        super().mousePressEvent(event)

    def _update_cursor(self):
        """Update cursor based on state"""
        if self._is_selected:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        elif self._beat_data:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def enterEvent(self, event):
        """Handle mouse enter events"""
        if not self._is_selected and self._beat_data:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave events"""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)

    def sizeHint(self) -> QSize:
        """Provide size hint for layout management"""
        return QSize(120, 120)

    def get_position_data(self) -> Optional[BeatData]:
        """Get the current position data"""
        return self._beat_data

    def clear_position_data(self):
        """Clear position data and show only START text (V1-style clear behavior)"""
        self._beat_data = None
        self._pictograph_data = None  # NEW: Also clear separate pictograph data
        self._position_key = None
        self._show_cleared_state()

        self.show()
        self.setVisible(True)
        print(
            f"🔧 [START_POS_VIEW] Start position view cleared and made visible: {self.isVisible()}"
        )

        parent = self.parent()
        parent_visible = parent.isVisible() if parent else "No parent"
        print(f"🔧 [START_POS_VIEW] Parent visibility: {parent_visible}")

    def _update_display(self):
        """Update the visual display based on position data"""
        if not self._beat_data and not self._position_key:
            self._show_empty_state()
            return

        self._update_pictograph()

    def _update_pictograph(self):
        """Update pictograph display using Modern pictograph component with START text overlay"""
        if not self._pictograph_component:
            return

        self._mark_overlay_invalid()

        # NEW APPROACH: Use separate pictograph data if available
        if hasattr(self, "_pictograph_data") and self._pictograph_data is not None:
            self._pictograph_component.update_pictograph(self._pictograph_data)
        elif self._beat_data:
            self._pictograph_component.update_pictograph(self._beat_data)
        else:
            self._pictograph_component.clear_pictograph()

        # CRITICAL FIX: Ensure pictograph component is visible when it has content
        self._pictograph_component.show()
        self._pictograph_component.setVisible(True)

        self._add_start_text_overlay()

    def _show_empty_state(self):
        """Show empty state when no position data"""
        self._mark_overlay_invalid()

        if self._pictograph_component:
            self._pictograph_component.clear_pictograph()

        self._add_start_text_overlay()

    def _show_cleared_state(self):
        """Show cleared state - blank white pictograph with START text overlay"""
        self._mark_overlay_invalid()

        if self._pictograph_component:
            # Clear any existing pictograph data
            self._pictograph_component.clear_pictograph()

            if (
                hasattr(self._pictograph_component, "scene")
                and self._pictograph_component.scene
            ):
                self._pictograph_component.scene.clear()

            # CRITICAL: Ensure pictograph component is visible to show blank white background
            self._pictograph_component.show()
            self._pictograph_component.setVisible(True)

        self._add_start_text_overlay()

    def _mark_overlay_invalid(self):
        """Mark the existing overlay as invalid before scene operations"""
        # No longer needed with unified widget approach - just cleanup
        self._cleanup_existing_overlay()

    def resizeEvent(self, event):
        """Handle resize events and update overlay scaling"""
        super().resizeEvent(event)
        self._update_overlay_scaling()

    def _update_overlay_scaling(self):
        """Update scaling for START text overlay"""
        if self._start_text_overlay and hasattr(
            self._start_text_overlay, "update_scaling"
        ):
            self._start_text_overlay.update_scaling()

    def setAccessibleName(self, name: str):
        """Set accessible name for screen readers"""
        super().setAccessibleName(name)
        if self._position_key:
            accessible_desc = f"Start position {self._position_key}"
        elif self._beat_data:
            accessible_desc = f"Start position with letter {self._beat_data.letter}"
        else:
            accessible_desc = "Start position not set, click to select"
        self.setAccessibleDescription(accessible_desc)

    def keyPressEvent(self, event):
        """Handle keyboard events"""
        from PyQt6.QtCore import Qt

        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.start_pos_beat_clicked.emit()
        super().keyPressEvent(event)

    def cleanup(self):
        """Cleanup resources when the view is being destroyed"""
        # Clean up overlays
        self._cleanup_existing_overlay()

        # Clean up selection overlay
        if self._selection_overlay:
            try:
                self._selection_overlay.deleteLater()
            except (RuntimeError, AttributeError):
                pass
            self._selection_overlay = None

        # Cleanup pictograph component
        if self._pictograph_component:
            self._pictograph_component.cleanup()
            self._pictograph_component = None

    def closeEvent(self, event):
        """Handle close event to cleanup resources"""
        self.cleanup()
        super().closeEvent(event)

    def __del__(self):
        """Destructor to ensure cleanup"""
        try:
            self.cleanup()
        except Exception:
            pass

    def set_loading_state(self, loading: bool):
        """Set loading state while position is being processed"""
        if loading:
            pass
        else:
            self._update_display()
