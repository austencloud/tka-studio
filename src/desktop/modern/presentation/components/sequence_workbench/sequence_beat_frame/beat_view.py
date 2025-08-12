"""
Modern Beat View Component

Individual beat widget for the Modern sequence workbench, replacing Legacy's BeatView
with modern architecture patterns and Modern pictograph integration.
"""

from __future__ import annotations

import contextlib

from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QColor, QPainter, QPen
from PyQt6.QtWidgets import QFileDialog, QFrame, QMenu, QMessageBox, QVBoxLayout

from desktop.modern.domain.models import BeatData

from .beat_number_overlay import BeatNumberOverlay, add_beat_number_to_view
from .selection_overlay import SelectionOverlay
from .start_text_overlay import StartTextOverlay
from ...pictograph.views import create_beat_view
from ...pictograph.views.beat_pictograph_view import BeatPictographView


class BeatView(QFrame):
    """
    Modern beat view widget with Modern pictograph integration.

    Replaces Legacy's BeatView with:
    - Clean separation of concerns
    - Modern pictograph rendering integration
    - Modern PyQt6 patterns
    - Responsive design
    """

    # Additional signals specific to beat view
    beat_clicked = pyqtSignal()
    beat_modified = pyqtSignal(object)  # BeatData object
    beat_context_menu = pyqtSignal()

    def __init__(self, beat_number: int, parent=None):
        super().__init__(parent)

        # Beat-specific properties
        self._beat_number = beat_number

        # Common state (previously from PictographViewBase)
        self._beat_data: BeatData | None = None
        self._is_selected = False
        self._is_highlighted = False

        # UI components
        self._pictograph_component: BeatPictographView | None = None
        self._selection_overlay: SelectionOverlay | None = None

        # START text overlay for preserved start position beat
        self._start_text_overlay: StartTextOverlay | None = None
        self._show_start_text = False

        # Beat number overlay for sequence beats
        self._beat_number_overlay: BeatNumberOverlay | None = None
        self._show_beat_number = False

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

        # Create direct pictograph view for beat frame (no widget wrapper)
        self._pictograph_component = create_beat_view(parent=self)
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
        """Update the pictograph display with current beat data"""
        if self._pictograph_component and self._beat_data:
            self._pictograph_component.update_from_beat(self._beat_data)
        elif self._pictograph_component:
            self._pictograph_component.clear_pictograph()

    # Direct view handles its own scaling and styling - no configuration needed

    # State management
    def set_beat_data(self, beat_data: BeatData | None):
        """Set beat data and update display."""
        if self._beat_data != beat_data:
            self._beat_data = beat_data
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

    def set_beat_number_visible(self, visible: bool):
        """Set whether beat number overlay should be visible"""
        if self._show_beat_number != visible:
            self._show_beat_number = visible
            self._update_beat_number_overlay()

    # Display updates
    def _update_display(self):
        """Update the visual display based on beat data"""
        if not self._beat_data:
            self._show_empty_state()
            return

        # No beat label in legacy - beat numbers are rendered on the pictograph scene
        # Update pictograph with beat data
        self._update_pictograph()

    def _update_pictograph(self):
        """Update pictograph display using Modern pictograph component"""
        if not self._beat_data or not self._pictograph_component:
            return

        # Update the pictograph component with beat data
        self._pictograph_component.update_pictograph(self._beat_data)

        # Update START text overlay (mutual exclusivity with beat content)
        self._update_start_text_overlay()

        # Update beat number overlay
        self._update_beat_number_overlay()

    def _show_empty_state(self):
        """Show empty state when no beat data"""
        # No beat label in legacy - just clear the pictograph

        # Clear pictograph component
        if self._pictograph_component:
            self._pictograph_component.clear_pictograph()

        # Update START text overlay if needed
        self._update_start_text_overlay()

    def _update_start_text_overlay(self):
        """Update START text overlay based on current state"""
        if not self._pictograph_component:
            return

        # Get the scene from the PictographWidget
        scene = getattr(self._pictograph_component, "scene", None)
        if not scene:
            return

        # Clean up existing overlay
        self._cleanup_start_text_overlay()

        # Show START text if enabled (for preserved start position beat)
        if self._show_start_text:
            try:
                # Create overlay with scene as parent for Qt lifecycle management
                self._start_text_overlay = StartTextOverlay(scene)

                # Set the BeatView as the widget parent for proper cleanup
                self._start_text_overlay.setParent(self)

                self._start_text_overlay.show_start_text()
            except Exception as e:
                print(f"Failed to create START text overlay on beat: {e}")
                self._start_text_overlay = None

    def _cleanup_start_text_overlay(self):
        """Safely cleanup existing START text overlay"""
        if not self._start_text_overlay:
            return

        # Mark as invalid immediately to prevent further access
        if hasattr(self._start_text_overlay, "_is_valid"):
            self._start_text_overlay._is_valid = False

        # Clear our reference and let Qt's garbage collection handle the rest
        self._start_text_overlay = None

    def _update_beat_number_overlay(self):
        """Update beat number overlay based on current state"""
        # Clean up existing overlay
        self._cleanup_beat_number_overlay()

        # Show beat number if enabled and we have beat data (mutual exclusivity with START text)
        if self._show_beat_number and self._beat_data and not self._show_start_text:
            try:
                self._beat_number_overlay = add_beat_number_to_view(
                    self, self._beat_number
                )
            except Exception as e:
                print(
                    f"Failed to create beat number overlay on beat {self._beat_number}: {e}"
                )
                self._beat_number_overlay = None

    def _cleanup_beat_number_overlay(self):
        """Safely cleanup existing beat number overlay"""
        if not self._beat_number_overlay:
            return

        try:
            # Hide and delete the overlay
            self._beat_number_overlay.hide_beat_number()
            self._beat_number_overlay.deleteLater()
        except Exception as e:
            print(f"Error cleaning up beat number overlay: {e}")
        finally:
            self._beat_number_overlay = None

    # Override mouse press to emit specific signals
    def mousePressEvent(self, event):
        """Handle mouse press events"""
        from PyQt6.QtCore import Qt

        if event.button() == Qt.MouseButton.LeftButton:
            self.beat_clicked.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            # Show context menu if beat has data
            if self._beat_data:
                self._show_context_menu(event.globalPosition().toPoint())
            else:
                self.beat_context_menu.emit()

        # Also emit the base class signal
        super().mousePressEvent(event)

    def _show_context_menu(self, global_pos):
        """Show context menu for beat export"""
        menu = QMenu(self)

        # Export action
        export_action = QAction("Export Beat as Image...", self)
        export_action.triggered.connect(self._export_beat)
        menu.addAction(export_action)

        # Show menu
        menu.exec(global_pos)

    def _export_beat(self):
        """Export this individual beat as an image"""
        if not self._beat_data:
            QMessageBox.warning(self, "Export Error", "No beat data to export.")
            return

        # Get save file path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            f"Export Beat {self._beat_number}",
            f"beat_{self._beat_number}.png",
            "PNG Images (*.png);;All Files (*)",
        )

        if not file_path:
            return  # User cancelled

        try:
            # Create a single-beat sequence for export
            single_beat_sequence = [self._beat_data.to_dict()]

            # Import export service
            from datetime import datetime
            from pathlib import Path

            from desktop.modern.core.dependency_injection.di_container import (
                DIContainer,
            )
            from desktop.modern.core.dependency_injection.image_export_service_registration import (
                register_image_export_services,
            )
            from desktop.modern.core.interfaces.image_export_services import (
                ImageExportOptions,
                ISequenceImageExporter,
            )

            # Setup export service
            container = DIContainer()
            register_image_export_services(container)
            export_service = container.resolve(ISequenceImageExporter)

            # Create export options for single beat
            options = ImageExportOptions(
                add_word=False,  # No word for single beat
                add_user_info=False,  # No user info for single beat
                add_difficulty_level=False,  # No difficulty for single beat
                add_beat_numbers=True,  # Show beat number
                add_reversal_symbols=True,  # Show reversals if any
                include_start_position=False,  # No start position for single beat
                user_name="",
                export_date=datetime.now().strftime("%m-%d-%Y"),
                notes=f"Single beat export - Beat {self._beat_number}",
            )

            # Export the beat
            result = export_service.export_sequence_image(
                single_beat_sequence,
                f"Beat_{self._beat_number}",
                Path(file_path),
                options,
            )

            if result.success:
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Beat {self._beat_number} exported successfully to:\n{file_path}",
                )
            else:
                QMessageBox.warning(
                    self,
                    "Export Failed",
                    f"Failed to export beat: {result.error_message}",
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Error",
                f"An error occurred while exporting the beat:\n{e!s}",
            )

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

    def cleanup(self):
        """Cleanup resources when the view is being destroyed"""
        # Clean up selection overlay
        if self._selection_overlay:
            with contextlib.suppress(RuntimeError, AttributeError):
                self._selection_overlay.deleteLater()
            self._selection_overlay = None

        # Cleanup pictograph component
        if self._pictograph_component:
            self._pictograph_component.cleanup()
            self._pictograph_component = None

    def paintEvent(self, event):
        """Custom paint event for additional visual effects"""
        super().paintEvent(event)

        # Add selection indicator if selected
        if self._is_selected:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw selection indicator in top-right corner
            pen = QPen(QColor(74, 144, 226), 3)
            painter.setPen(pen)

            # Draw a small circle indicator
            indicator_size = 8
            x = self.width() - indicator_size - 4
            y = 4
            painter.drawEllipse(x, y, indicator_size, indicator_size)

    def _update_overlay_scaling(self):
        """Update scaling for all text overlays"""
        # Update beat number overlay scaling
        if self._beat_number_overlay and hasattr(
            self._beat_number_overlay, "update_scaling"
        ):
            self._beat_number_overlay.update_scaling()

        # Update START text overlay scaling
        if self._start_text_overlay and hasattr(
            self._start_text_overlay, "update_scaling"
        ):
            self._start_text_overlay.update_scaling()

    # Accessibility support
    def setAccessibleName(self, name: str):
        """Set accessible name for screen readers"""
        super().setAccessibleName(name)
        if self._beat_data:
            accessible_desc = f"Beat {self._beat_number}, Letter {self._beat_data.letter}, Duration {self._beat_data.duration}"
        else:
            accessible_desc = f"Empty beat slot {self._beat_number}"
        self.setAccessibleDescription(accessible_desc)

    # Cleanup and lifecycle management
    def cleanup(self):
        """Cleanup resources when the view is being destroyed"""
        self._cleanup_start_text_overlay()
        self._cleanup_beat_number_overlay()
        super().cleanup()

    def closeEvent(self, event):
        """Handle close event to cleanup resources"""
        self.cleanup()
        super().closeEvent(event)

    def __del__(self):
        """Destructor to ensure cleanup"""
        with contextlib.suppress(Exception):
            self.cleanup()
