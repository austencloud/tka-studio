"""
Real Pictograph Preview Component for Visibility Settings.

Uses modern PictographScene with modular renderers to show actual pictograph
that updates in real-time as visibility settings change.
"""

from __future__ import annotations

import logging

from PyQt6.QtCore import QPropertyAnimation, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from desktop.modern.domain.models import (
    BeatData,
    Location,
    MotionData,
    MotionType,
    RotationDirection,
)
from desktop.modern.domain.models.enums import Orientation
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.pictograph.views import (
    BasePictographView,
    create_pictograph_view,
)


logger = logging.getLogger(__name__)


class VisibilityPictographPreview(QWidget):
    """
    Real pictograph preview component that shows actual TKA pictograph
    with all elements and updates in real-time as visibility changes.
    """

    preview_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pictograph_view: BasePictographView | None = None
        self.sample_beat_data: BeatData | None = None

        # Animation properties
        self._fade_animations: dict[str, QPropertyAnimation] = {}
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._perform_delayed_update)

        self._setup_ui()
        self._create_sample_data()
        self._initialize_widget()

    def _setup_ui(self):
        """Setup the compact UI layout for settings dialog."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Very compact margins
        layout.setSpacing(0)  # Minimal spacing

        # Create pictograph view (much smaller for settings dialog)
        self.pictograph_view = create_pictograph_view("base", parent=self)
        self.pictograph_view.setMinimumSize(
            180, 140
        )  # Much smaller for settings dialog
        # set the aspect ratio to 1:1
        self.pictograph_view.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.pictograph_view)

        # Compact info label
        info_label = QLabel("Live preview")
        info_label.setObjectName("preview_info")
        info_label.setFont(QFont("Arial", 9))  # Smaller font
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        self._apply_styling()

    def _apply_styling(self):
        """Apply modern glassmorphism styling."""
        self.setStyleSheet(
            """
            QWidget {
                background: rgba(255, 255, 255, 0.1);
                color: white;
            }

            QLabel#preview_title {
                background: transparent;
                border: none;
                color: rgba(255, 255, 255, 0.9);
                font-weight: bold;
                margin-bottom: 5px;
            }

            QLabel#preview_info {
                background: transparent;
                border: none;
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                font-style: italic;
                margin-top: 5px;
            }

            QGraphicsView {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
            }
        """
        )

    def _create_sample_data(self):
        """Create authentic TKA pictograph data based on real Alpha 1-3 sequence."""
        try:
            # Blue motion: pro, clockwise, west to north (basic positioning)
            blue_motion = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                turns=0.0,  # Basic positioning without turns
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
            )

            # Red motion: pro, clockwise, east to south (basic positioning)
            red_motion = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=0.0,  # Basic positioning without turns
                start_ori=Orientation.IN,
                end_ori=Orientation.IN,
            )

            # Glyph data is no longer needed - all derived data now comes from PictographData

            motions = {
                "blue": blue_motion,
                "red": red_motion,
            }
            from desktop.modern.domain.models.enums import (
                Direction,
                GridPosition,
                LetterType,
                Timing,
            )

            self.sample_pictograph_data = PictographData(
                motions=motions,
                letter="A",
                start_position=GridPosition.ALPHA1,
                end_position=GridPosition.ALPHA3,
                timing=Timing.SPLIT,
                direction=Direction.SAME,
                letter_type=LetterType.TYPE1,
                is_blank=False,
                metadata={
                    "preview_mode": True,
                },
            )

            # Create comprehensive beat data
            self.sample_beat_data = BeatData(
                beat_number=1,
                duration=1.0,
                pictograph_data=self.sample_pictograph_data,
                blue_reversal=False,  # No reversals in basic Alpha sequence
                red_reversal=False,  # No reversals in basic Alpha sequence
                is_blank=False,
                metadata={
                    "preview_mode": True,
                    "start_position": "alpha1",
                    "end_position": "alpha3",
                    "timing": "split",
                    "direction": "same",
                },
            )

        except Exception as e:
            logger.exception(f"Error creating sample data: {e}")
            # Create minimal fallback data
            self.sample_beat_data = BeatData(beat_number=1, is_blank=True)

    def _initialize_widget(self):
        """Initialize the pictograph view with sample data."""
        try:
            # Update view with sample data
            if self.sample_beat_data and self.sample_beat_data.pictograph_data:
                self.pictograph_view.update_from_pictograph_data(
                    self.sample_beat_data.pictograph_data
                )

            logger.debug("Initialized pictograph view for preview")

        except Exception as e:
            logger.exception(f"Error initializing view: {e}")

    # _fit_view method removed - PictographWidget handles scaling automatically

    def update_visibility(self, element_type: str, visible: bool, animate: bool = True):
        """
        Update visibility of specific element type with optional animation.

        Args:
            element_type: Type of element (TKA, VTG, Elemental, Positions, red_motion, blue_motion, etc.)
            visible: Whether element should be visible
            animate: Whether to animate the change
        """
        if not self.pictograph_view or not self.pictograph_view.scene:
            return

        try:
            # Map element types to scene visibility categories
            if element_type in ["TKA", "VTG", "Elemental", "Positions", "Reversals"]:
                # Glyph visibility
                self.pictograph_view.scene.update_visibility(
                    "glyph", element_type, visible
                )
            elif element_type in ["red_motion", "blue_motion"]:
                # Motion visibility
                color = element_type.replace("_motion", "")
                self.pictograph_view.scene.update_visibility("motion", color, visible)
            elif element_type in ["grid", "props", "arrows", "non_radial"]:
                # Other element visibility
                self.pictograph_view.scene.update_visibility(
                    "other", element_type, visible
                )
            else:
                logger.warning(
                    f"Unknown element type for visibility update: {element_type}"
                )
                return

            # Schedule delayed update to avoid rapid successive updates
            if animate:
                self._schedule_delayed_update()
            else:
                self._perform_immediate_update()

            logger.debug(f"Updated {element_type} visibility to {visible}")

        except Exception as e:
            logger.exception(f"Error updating visibility for {element_type}: {e}")

    def _schedule_delayed_update(self):
        """Schedule a delayed update to batch rapid changes."""
        self._update_timer.stop()
        self._update_timer.start(100)  # 100ms delay

    def _perform_delayed_update(self):
        """Perform the actual scene update."""
        self._perform_immediate_update()

    def _perform_immediate_update(self):
        """Immediately update the view with current data."""
        if (
            self.pictograph_view
            and self.sample_beat_data
            and self.sample_beat_data.pictograph_data
        ):
            try:
                self.pictograph_view.update_from_pictograph_data(
                    self.sample_beat_data.pictograph_data
                )
                self.preview_updated.emit()
            except Exception as e:
                logger.exception(f"Error updating view: {e}")

    def refresh_preview(self):
        """Force refresh the entire preview."""
        self._perform_immediate_update()

    def cleanup(self):
        """Clean up resources."""
        try:
            self._update_timer.stop()

            # Clear animations
            for animation in self._fade_animations.values():
                animation.stop()
            self._fade_animations.clear()

            # Clean up view
            if self.pictograph_view:
                self.pictograph_view.cleanup()
                self.pictograph_view = None

        except Exception as e:
            logger.exception(f"Error during cleanup: {e}")
