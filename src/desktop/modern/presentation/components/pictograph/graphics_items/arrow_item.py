"""
Enhanced Self-Contained Arrow Graphics Item

Self-sufficient arrow that handles its own rendering logic by calling the business layer.
Eliminates the need for orchestrator classes while maintaining clean separation.
"""

from __future__ import annotations

import logging
import os
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from desktop.modern.application.services.pictograph.arrow_rendering_service import (
    ArrowRenderingService,
)
from desktop.modern.core.dependency_injection.di_container import get_container
from desktop.modern.core.interfaces.positioning_services import (
    IArrowCoordinateSystemService,
    IArrowPositioningOrchestrator,
)
from desktop.modern.domain.models.arrow_data import ArrowData
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.pictograph_data import PictographData


logger = logging.getLogger(__name__)


class ArrowItem(QGraphicsSvgItem):
    """
    Self-contained arrow graphics item that handles its own rendering logic.

    Uses business logic services for positioning and asset management while
    handling Qt-specific operations internally.
    """

    def __init__(
        self,
        color: str | None = None,
        motion_data: MotionData = None,
        pictograph_data: PictographData = None,
        parent=None,
    ):
        super().__init__(parent)

        # Arrow data
        self.arrow_color: str | None = color
        self.motion_data = motion_data
        self.pictograph_data = pictograph_data

        # Selection and highlighting properties
        self.is_highlighted = False
        self.highlight_color = QColor("#FFD700")  # Gold
        self.highlight_pen_width = 3

        # Business logic service
        self._arrow_renderer = ArrowRenderingService()

        # Positioning services from DI container
        self._positioning_orchestrator = None
        self._coordinate_system = None
        self._resolve_positioning_services()

        # Default: arrows are NOT selectable (safe default)
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, False)
        self.setAcceptHoverEvents(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Set up the arrow if we have the required data
        if color and motion_data:
            self._setup_arrow()

    def _resolve_positioning_services(self):
        """Resolve positioning services from DI container."""
        try:
            container = get_container()
            self._positioning_orchestrator = container.resolve(
                IArrowPositioningOrchestrator
            )
            self._coordinate_system = container.resolve(IArrowCoordinateSystemService)
        except Exception as e:
            logger.debug(f"Positioning services not available: {e}")
            # Services are optional - arrow will use fallback positioning

    def _setup_arrow(self):
        """Set up the arrow using business logic and Qt operations."""
        if not self.arrow_color or not self.motion_data:
            logger.warning("Cannot setup arrow: missing color or motion data")
            return

        # Business Logic: Validate motion visibility
        if not self._arrow_renderer.validate_motion_visibility(self.motion_data):
            self.setVisible(False)
            return

        # Business Logic: Get SVG path and load renderer
        svg_renderer = self._load_svg_renderer()
        if not svg_renderer:
            logger.error(f"Failed to load SVG renderer for {self.arrow_color} arrow")
            return

        # Qt Operation: Set the renderer
        self.setSharedRenderer(svg_renderer)

        # Business Logic: Calculate position and apply transforms
        self._calculate_and_apply_position()

    def _load_svg_renderer(self) -> QSvgRenderer | None:
        """Load SVG renderer using business logic for asset management."""
        # Business Logic: Get primary SVG path
        arrow_svg_path = self._arrow_renderer.asset_manager.get_arrow_svg_path(
            self.motion_data, self.arrow_color
        )

        # Try pre-colored SVG first
        if os.path.exists(arrow_svg_path):
            renderer = QSvgRenderer(arrow_svg_path)
            if renderer.isValid():
                return renderer

        # Fallback: Use original SVG with color transformation
        original_svg_path = (
            self._arrow_renderer.asset_manager.get_fallback_arrow_svg_path(
                self.motion_data
            )
        )

        if os.path.exists(original_svg_path):
            # Business Logic: Load and transform SVG data
            svg_data = self._arrow_renderer.load_cached_svg_data(original_svg_path)
            if svg_data:
                colored_svg_data = (
                    self._arrow_renderer.asset_manager.apply_color_transformation(
                        svg_data, self.arrow_color
                    )
                )

                # Qt Operation: Create renderer from transformed data
                renderer = QSvgRenderer(bytearray(colored_svg_data, encoding="utf-8"))
                if renderer.isValid():
                    return renderer

        logger.error(
            f"No valid SVG found for {self.arrow_color} arrow with motion: {self.motion_data}"
        )
        return None

    def _calculate_and_apply_position(self):
        """Calculate position using business logic and apply Qt transforms."""
        # CRITICAL FIX: Check if arrow data already has pre-calculated positions
        existing_arrow_data = None
        if (
            self.pictograph_data
            and hasattr(self.pictograph_data, "arrows")
            and self.pictograph_data.arrows
            and self.arrow_color in self.pictograph_data.arrows
        ):
            existing_arrow_data = self.pictograph_data.arrows[self.arrow_color]

        # Use pre-calculated positions if available (from generation pipeline)
        if (
            existing_arrow_data
            and existing_arrow_data.position_x != 0.0
            and existing_arrow_data.position_y != 0.0
        ):
            position_x = existing_arrow_data.position_x
            position_y = existing_arrow_data.position_y
            rotation = existing_arrow_data.rotation_angle
            logger.debug(
                f"✅ Using pre-calculated position for {self.arrow_color}: ({position_x}, {position_y}, {rotation}°)"
            )
        else:
            # Fallback: Calculate position using orchestrator
            arrow_data = ArrowData(
                color=self.arrow_color,
                turns=getattr(self.motion_data, "turns", 0),
                is_visible=True,
            )
            # Delegate directly to the positioning orchestrator if available
            if self._positioning_orchestrator and self.pictograph_data:
                try:
                    motion_data = None
                    if (
                        hasattr(self.pictograph_data, "motions")
                        and self.pictograph_data.motions
                    ):
                        motion_data = self.pictograph_data.motions.get(arrow_data.color)

                    position_x, position_y, rotation = (
                        self._positioning_orchestrator.calculate_arrow_position(
                            arrow_data, self.pictograph_data, motion_data
                        )
                    )
                    logger.debug(
                        f"🔄 Calculated position for {self.arrow_color}: ({position_x}, {position_y}, {rotation}°)"
                    )

                except Exception as e:
                    logger.exception(f"Positioning orchestrator failed: {e}")
                    traceback.print_exc()
                    position_x, position_y, rotation = 475.0, 475.0, 0.0  # Fallback
                    logger.warning(
                        f"🚨 FALLBACK - {self.arrow_color}: Using center position (475, 475, 0°)"
                    )
            else:
                logger.warning("Using fallback arrow positioning (center)")
                position_x, position_y, rotation = 475.0, 475.0, 0.0
                logger.warning(
                    f"🚨 FALLBACK - {self.arrow_color}: Using center position (475, 475, 0°)"
                )

        # Qt Operations: Apply transforms
        self._apply_transforms(position_x, position_y, rotation)

        # Business Logic: Apply mirror transform if positioning orchestrator available
        if self._positioning_orchestrator:
            # Use existing arrow data if available, otherwise create new
            if existing_arrow_data:
                # Check if mirror state is already set in the data
                if existing_arrow_data.is_mirrored:
                    logger.debug(
                        f"✅ Using pre-calculated mirror state for {self.arrow_color}: {existing_arrow_data.is_mirrored}"
                    )
                    # Apply the pre-calculated mirror transformation
                    if existing_arrow_data.is_mirrored:
                        self._apply_mirror_transform()
                else:
                    # Calculate mirror state
                    should_mirror = self._positioning_orchestrator.should_mirror_arrow(
                        existing_arrow_data, self.pictograph_data
                    )
                    if should_mirror:
                        self._positioning_orchestrator.apply_mirror_transform(
                            self, should_mirror
                        )
            else:
                # Fallback: create arrow data for mirror calculation
                arrow_data_with_position = ArrowData(
                    color=self.arrow_color,
                    turns=getattr(self.motion_data, "turns", 0),
                    position_x=position_x,
                    position_y=position_y,
                    rotation_angle=rotation,
                    is_visible=True,
                )
                should_mirror = self._positioning_orchestrator.should_mirror_arrow(
                    arrow_data_with_position, self.pictograph_data
                )
                if should_mirror:
                    self._positioning_orchestrator.apply_mirror_transform(
                        self, should_mirror
                    )

        # Final positioning
        self._finalize_positioning(position_x, position_y)

    def _apply_mirror_transform(self):
        """Apply mirror transformation to the arrow."""
        # Apply horizontal flip transformation
        transform = self.transform()
        transform.scale(-1, 1)  # Flip horizontally
        self.setTransform(transform)

    def _apply_transforms(self, position_x: float, position_y: float, rotation: float):
        """Apply Qt-specific transforms to the arrow item."""
        # Set transform origin to arrow's visual center BEFORE rotation
        bounds = self.boundingRect()
        self.setTransformOriginPoint(bounds.center())

        # Apply rotation around the visual center
        self.setRotation(rotation)

    def _finalize_positioning(self, position_x: float, position_y: float):
        """Finalize arrow positioning in Qt scene coordinates."""
        # Get bounding rect AFTER all transformations (scaling + rotation)
        final_bounds = self.boundingRect()

        # Position so the arrow's visual center appears at the calculated position
        final_x = position_x - final_bounds.center().x()
        final_y = position_y - final_bounds.center().y()

        self.setPos(final_x, final_y)
        self.setZValue(100)  # Bring arrows to front

    # =============================================================================
    # PUBLIC INTERFACE METHODS
    # =============================================================================

    def update_arrow(
        self,
        color: str | None = None,
        motion_data: MotionData = None,
        pictograph_data: PictographData = None,
    ):
        """Update arrow properties and re-setup."""
        if color:
            self.arrow_color = color
        if motion_data:
            self.motion_data = motion_data
        if pictograph_data:
            self.pictograph_data = pictograph_data

        # Re-setup with new data
        if self.arrow_color and self.motion_data:
            self._setup_arrow()
            # CRITICAL FIX: Ensure positioning is calculated when arrow is updated with real data
            if self.pictograph_data and self.arrow_color:
                self._calculate_and_apply_position()
            else:
                logger.warning(
                    f"⚠️ POSITIONING SKIPPED - {self.arrow_color}: pictograph_data={self.pictograph_data is not None}, color={self.arrow_color}"
                )
        else:
            logger.warning(
                f"⚠️ SETUP SKIPPED - {self.arrow_color}: color={self.arrow_color}, motion_data={self.motion_data is not None}"
            )

    # =============================================================================
    # SELECTION AND INTERACTION METHODS (Preserved from original)
    # =============================================================================
    def mousePressEvent(self, event):
        """Handle mouse press - emit signal if selectable."""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.flags() & self.GraphicsItemFlag.ItemIsSelectable:
                # Arrow is selectable - emit signal
                if hasattr(self.scene(), "arrow_selected"):
                    self.scene().arrow_selected.emit(self.arrow_color)
                event.accept()
                return
            # Arrow not selectable - pass through
            event.ignore()
            return

        # For non-left clicks, use default behavior if selectable
        if self.flags() & self.GraphicsItemFlag.ItemIsSelectable:
            super().mousePressEvent(event)
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        """Handle mouse release - only if selectable."""
        if self.flags() & self.GraphicsItemFlag.ItemIsSelectable:
            super().mouseReleaseEvent(event)
        else:
            event.ignore()

    def hoverEnterEvent(self, event):
        """Handle hover enter - only if hover events enabled."""
        if self.acceptHoverEvents():
            super().hoverEnterEvent(event)
        else:
            event.ignore()

    def hoverLeaveEvent(self, event):
        """Handle hover leave - only if hover events enabled."""
        if self.acceptHoverEvents():
            super().hoverLeaveEvent(event)
        else:
            event.ignore()

    def add_selection_highlight(self, color: QColor = None):
        """Add selection highlighting."""
        if color:
            self.highlight_color = color
        self.is_highlighted = True
        self.update()

    def paint(self, painter, option, widget=None):
        """Custom paint to show selection highlight."""
        # Draw the SVG first
        super().paint(painter, option, widget)

        # Add highlight if selected
        if self.is_highlighted:
            painter.setPen(QPen(self.highlight_color, self.highlight_pen_width))
            painter.drawRect(self.boundingRect())
