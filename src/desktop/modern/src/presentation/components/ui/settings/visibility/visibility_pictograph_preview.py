"""
Real Pictograph Preview Component for Visibility Settings.

Uses modern PictographScene with modular renderers to show actual pictograph
that updates in real-time as visibility settings change.
"""

from typing import Optional, Dict
import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation
from PyQt6.QtGui import QFont

from domain.models.core_models import (
    BeatData,
    MotionData,
    GlyphData,
    MotionType,
    RotationDirection,
    Location,
    LetterType,
    VTGMode,
    ElementalType,
)
from presentation.components.pictograph.pictograph_scene import PictographScene

logger = logging.getLogger(__name__)


class VisibilityPictographPreview(QWidget):
    """
    Real pictograph preview component that shows actual TKA pictograph
    with all elements and updates in real-time as visibility changes.
    """

    preview_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene: Optional[PictographScene] = None
        self.view: Optional[QGraphicsView] = None
        self.sample_beat_data: Optional[BeatData] = None

        # Animation properties
        self._fade_animations: Dict[str, QPropertyAnimation] = {}
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._perform_delayed_update)

        self._setup_ui()
        self._create_sample_data()
        self._initialize_scene()

    def _setup_ui(self):
        """Setup the compact UI layout for settings dialog."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Very compact margins
        layout.setSpacing(0)  # Minimal spacing

        # Graphics view for pictograph scene (much smaller)
        self.view = QGraphicsView()
        self.view.setMinimumSize(180, 140)  # Much smaller for settings dialog
        # set the aspect ratio to 1:1
        self.view.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        from PyQt6.QtGui import QPainter

        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        layout.addWidget(self.view)

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
                start_ori="in",
                end_ori="in",
            )

            # Red motion: pro, clockwise, east to south (basic positioning)
            red_motion = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=0.0,  # Basic positioning without turns
                start_ori="in",
                end_ori="in",
            )

            # Create comprehensive glyph data with all elements
            glyph_data = GlyphData(
                vtg_mode=VTGMode.SPLIT_SAME,
                elemental_type=ElementalType.WATER,
                letter_type=LetterType.TYPE1,
                has_dash=False,  # "A" doesn't have dash
                turns_data="(0.0, 0.0)",  # Basic positioning without turns
                start_position="alpha1",
                end_position="alpha3",
                show_elemental=True,
                show_vtg=True,
                show_tka=True,
                show_positions=True,
            )

            # Create comprehensive beat data
            self.sample_beat_data = BeatData(
                beat_number=1,
                letter="A",
                duration=1.0,
                blue_motion=blue_motion,
                red_motion=red_motion,
                glyph_data=glyph_data,
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
            logger.error(f"Error creating sample data: {e}")
            # Create minimal fallback data
            self.sample_beat_data = BeatData(beat_number=1, letter="A", is_blank=True)

    def _initialize_scene(self):
        """Initialize the pictograph scene with sample data."""
        try:
            self.scene = PictographScene()
            self.view.setScene(self.scene)

            # Update scene with sample data
            if self.sample_beat_data:
                self.scene.update_beat(self.sample_beat_data)

            # Fit the view to show the entire pictograph
            self._fit_view()

            logger.debug("Initialized pictograph scene for preview")

        except Exception as e:
            logger.error(f"Error initializing scene: {e}")

    def _fit_view(self):
        """Fit the view to show the entire pictograph optimally."""
        if self.scene and self.view:
            # Get scene bounds and add some padding
            scene_rect = self.scene.itemsBoundingRect()
            if not scene_rect.isEmpty():
                # Add 10% padding around the content
                padding = max(scene_rect.width(), scene_rect.height()) * 0.1
                padded_rect = scene_rect.adjusted(-padding, -padding, padding, padding)
                self.view.fitInView(padded_rect, Qt.AspectRatioMode.KeepAspectRatio)
            else:
                # Fallback to scene rect if no items
                self.view.fitInView(
                    self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio
                )

    def update_visibility(self, element_type: str, visible: bool, animate: bool = True):
        """
        Update visibility of specific element type with optional animation.

        Args:
            element_type: Type of element (TKA, VTG, Elemental, Positions, red_motion, blue_motion, etc.)
            visible: Whether element should be visible
            animate: Whether to animate the change
        """
        if not self.scene:
            return

        try:
            # Update glyph data for the next render
            if self.sample_beat_data and self.sample_beat_data.glyph_data:
                glyph_data = self.sample_beat_data.glyph_data

                # Update visibility flags in glyph data using dataclasses.replace
                from dataclasses import replace

                if element_type == "TKA":
                    glyph_data = replace(glyph_data, show_tka=visible)
                elif element_type == "VTG":
                    glyph_data = replace(glyph_data, show_vtg=visible)
                elif element_type == "Elemental":
                    glyph_data = replace(glyph_data, show_elemental=visible)
                elif element_type == "Positions":
                    glyph_data = replace(glyph_data, show_positions=visible)

                # Update beat data with new glyph data
                self.sample_beat_data = self.sample_beat_data.update(
                    glyph_data=glyph_data
                )

            # Handle motion visibility by updating motion data
            if element_type in ["red_motion", "blue_motion"]:
                color = element_type.split("_")[0]
                if not visible:
                    # Remove motion data
                    if color == "red":
                        self.sample_beat_data = self.sample_beat_data.update(
                            red_motion=None
                        )
                    else:
                        self.sample_beat_data = self.sample_beat_data.update(
                            blue_motion=None
                        )
                else:
                    # Restore motion data (recreate if needed)
                    if color == "red" and not self.sample_beat_data.red_motion:
                        red_motion = MotionData(
                            motion_type=MotionType.PRO,
                            prop_rot_dir=RotationDirection.CLOCKWISE,
                            start_loc=Location.NORTH,
                            end_loc=Location.EAST,
                            turns=0.0,
                        )
                        self.sample_beat_data = self.sample_beat_data.update(
                            red_motion=red_motion
                        )
                    elif color == "blue" and not self.sample_beat_data.blue_motion:
                        blue_motion = MotionData(
                            motion_type=MotionType.PRO,
                            prop_rot_dir=RotationDirection.CLOCKWISE,
                            start_loc=Location.SOUTH,
                            end_loc=Location.WEST,
                            turns=0.0,
                        )
                        self.sample_beat_data = self.sample_beat_data.update(
                            blue_motion=blue_motion
                        )

            # Schedule delayed update to avoid rapid successive updates
            if animate:
                self._schedule_delayed_update()
            else:
                self._perform_immediate_update()

            logger.debug(f"Updated {element_type} visibility to {visible}")

        except Exception as e:
            logger.error(f"Error updating visibility for {element_type}: {e}")

    def _schedule_delayed_update(self):
        """Schedule a delayed update to batch rapid changes."""
        self._update_timer.stop()
        self._update_timer.start(100)  # 100ms delay

    def _perform_delayed_update(self):
        """Perform the actual scene update."""
        self._perform_immediate_update()

    def _perform_immediate_update(self):
        """Immediately update the scene with current data."""
        if self.scene and self.sample_beat_data:
            try:
                self.scene.update_beat(self.sample_beat_data)
                self.preview_updated.emit()
            except Exception as e:
                logger.error(f"Error updating scene: {e}")

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

            # Clean up scene
            if self.scene:
                self.scene.clear()
                self.scene = None

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
