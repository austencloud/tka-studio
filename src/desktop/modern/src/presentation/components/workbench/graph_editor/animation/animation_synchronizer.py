"""
Animation Synchronizer
=====================

Synchronizes toggle tab position with graph editor animations. Extracted from the original
animation controller to provide focused, single-responsibility synchronization logic.

This class handles:
- Real-time toggle tab position synchronization during animations
- Toggle tab animation setup and coordination
- Position calculations for synchronized movement
- Animation progress tracking for synchronization
"""

from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtWidgets import QWidget
import logging

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor

# Set up synchronizer logger
sync_logger = logging.getLogger("tka.animation.sync")


class AnimationSynchronizer:
    """Synchronizes toggle tab position with graph editor animations"""

    def __init__(self, graph_editor: "GraphEditor"):
        self._graph_editor = graph_editor
        self._toggle_position_animation: Optional[QPropertyAnimation] = None

    def start_synchronized_animations(
        self, height_animation: QPropertyAnimation, is_showing: bool
    ) -> None:
        """
        Start synchronized animations for graph editor and toggle tab.
        This replicates the legacy behavior where both animate simultaneously.
        """
        # Clean up any previous toggle animation
        if self._toggle_position_animation:
            self._toggle_position_animation.stop()
            self._toggle_position_animation = None
            sync_logger.debug("Cleaned up previous toggle animation")

        # Start the height animation
        height_animation.start()

        # Set up toggle tab animation if toggle tab exists
        toggle_tab = getattr(self._graph_editor, "_toggle_tab", None)
        if toggle_tab:
            self._animate_toggle_tab_position(is_showing, height_animation)

    def _animate_toggle_tab_position(
        self, is_showing: bool, height_animation: QPropertyAnimation
    ) -> None:
        """
        Animate toggle tab position synchronized with graph editor animation.
        Uses the same timing and easing as the legacy implementation.
        """
        toggle_tab = self._graph_editor._toggle_tab
        parent = self._graph_editor._parent_workbench

        if not parent:
            return

        parent_height = parent.height()
        toggle_height = toggle_tab.height()
        x = toggle_tab.x()

        # Calculate start and end positions based on animation direction
        if is_showing:
            # Show animation: toggle moves up as graph editor expands
            start_y = parent_height - toggle_height

            # Get target height from animation
            animation_target_height = height_animation.endValue()
            target_graph_bottom_y = parent_height - animation_target_height
            end_y = target_graph_bottom_y - toggle_height

            sync_logger.debug(
                "Toggle show animation: parent_h=%d, target_graph_h=%d, toggle_h=%d",
                parent_height,
                animation_target_height,
                toggle_height,
            )
            sync_logger.debug(
                "Calculated positions: start_y=%d, end_y=%d", start_y, end_y
            )
        else:
            # Hide animation: toggle moves down as graph editor collapses
            current_toggle_y = toggle_tab.y()
            start_y = current_toggle_y
            end_y = parent_height - toggle_height

            sync_logger.debug(
                "Toggle hide animation: current_y=%d, target_y=%d",
                current_toggle_y,
                end_y,
            )

        # Ensure positions are within valid bounds
        start_y = max(0, min(start_y, parent_height - toggle_height))
        end_y = max(0, min(end_y, parent_height - toggle_height))

        start_pos = QPoint(x, start_y)
        end_pos = QPoint(x, end_y)

        # Create toggle position animation
        if not self._toggle_position_animation:
            self._toggle_position_animation = QPropertyAnimation(toggle_tab, b"pos")

        self._toggle_position_animation.setDuration(400)  # Match graph editor animation
        self._toggle_position_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._toggle_position_animation.setStartValue(start_pos)
        self._toggle_position_animation.setEndValue(end_pos)

        animation_type = "toggle_tab_show" if is_showing else "toggle_tab_hide"
        sync_logger.debug(
            "Starting %s animation: %s → %s", animation_type, start_pos, end_pos
        )

        # Connect real-time synchronization
        height_animation.valueChanged.connect(
            lambda height: self.sync_toggle_to_graph_height(height, is_showing)
        )

        sync_logger.debug(
            "Using real-time synchronization instead of separate toggle animation"
        )

        sync_logger.debug(
            "Both animations started - Graph: %s, Toggle: %s",
            height_animation.state(),
            self._toggle_position_animation.state(),
        )

    def sync_toggle_to_graph_height(self, graph_height: int, is_showing: bool) -> None:
        """Synchronize toggle tab position to actual graph editor height in real-time"""
        toggle_tab = getattr(self._graph_editor, "_toggle_tab", None)
        if not toggle_tab:
            return

        parent = self._graph_editor._parent_workbench
        if not parent:
            return

        toggle_height = toggle_tab.height()
        graph_editor_rect = self._graph_editor.geometry()

        if graph_editor_rect.height() <= 0:
            sync_logger.warning(
                "Graph editor has invalid geometry: %s", graph_editor_rect
            )
            return

        workbench_pos = self._graph_editor.mapTo(parent, graph_editor_rect.topLeft())

        sync_logger.debug(
            "Graph editor rect: %s, workbench_pos: %s", graph_editor_rect, workbench_pos
        )

        # Calculate target toggle position
        target_y = workbench_pos.y() - toggle_height
        new_pos = QPoint(toggle_tab.x(), target_y)

        # Only move if there's a significant difference (avoid jitter)
        current_pos = toggle_tab.pos()
        if abs(current_pos.y() - target_y) > 2:
            toggle_tab.move(new_pos)
            sync_logger.debug(
                "Real-time sync: graph_h=%d, graph_top=%d, toggle_y=%d",
                graph_height,
                workbench_pos.y(),
                target_y,
            )

    def enable_real_time_sync(self) -> None:
        """Enable real-time synchronization mode on toggle tab"""
        toggle_tab = getattr(self._graph_editor, "_toggle_tab", None)
        if toggle_tab and hasattr(toggle_tab, "set_real_time_sync_active"):
            toggle_tab.set_real_time_sync_active(True)

    def disable_real_time_sync(self) -> None:
        """Disable real-time synchronization mode on toggle tab"""
        toggle_tab = getattr(self._graph_editor, "_toggle_tab", None)
        if toggle_tab and hasattr(toggle_tab, "set_real_time_sync_active"):
            toggle_tab.set_real_time_sync_active(False)

    def cleanup(self) -> None:
        """Clean up animation resources"""
        if self._toggle_position_animation:
            self._toggle_position_animation.stop()
            self._toggle_position_animation.deleteLater()
            self._toggle_position_animation = None

    def calculate_toggle_progress(
        self, start_pos: QPoint, end_pos: QPoint, current_pos: QPoint
    ) -> float:
        """Calculate animation progress for toggle tab"""
        if (
            not start_pos
            or not end_pos
            or not current_pos
            or start_pos.y() == end_pos.y()
        ):
            return 1.0

        total_distance = abs(end_pos.y() - start_pos.y())
        if total_distance == 0:
            return 1.0

        current_distance = abs(current_pos.y() - start_pos.y())
        return min(1.0, current_distance / total_distance)
