"""
Animation Size Calculator
========================

Handles all size calculations and workbench tracking for graph editor animations.
Extracted from the original animation controller to provide focused, single-responsibility
size management without animation interference.

This class is responsible for:
- Calculating preferred height based on workbench dimensions
- Tracking workbench size changes
- Providing size calculations without animation state dependencies
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor


class AnimationSizeCalculator:
    """Handles all size calculations and workbench tracking"""

    def __init__(self, graph_editor: "GraphEditor"):
        self._graph_editor = graph_editor
        self._workbench_width = 800
        self._workbench_height = 600

    def update_workbench_size(self, width: int, height: int) -> None:
        """Update workbench size reference for height calculations"""
        old_width, old_height = self._workbench_width, self._workbench_height
        self._workbench_width = width
        self._workbench_height = height

        # Log size change for debugging
        is_visible = (
            hasattr(self._graph_editor, "_state_manager")
            and self._graph_editor.state_manager.is_visible()
        )

        print(
            f"🔍 [HEIGHT DEBUG] Workbench size update: {old_width}x{old_height} -> {width}x{height} (visible={is_visible})"
        )

    def get_preferred_height(self) -> int:
        """Calculate preferred height based on workbench dimensions"""
        return min(int(self._workbench_height // 3.5), self._workbench_width // 4)

    def should_recalculate_size(
        self, is_animating: bool, is_cooldown_active: bool
    ) -> bool:
        """Determine if size should be recalculated based on animation state"""
        is_visible = (
            hasattr(self._graph_editor, "_state_manager")
            and self._graph_editor.state_manager.is_visible()
        )

        if not is_visible:
            print(
                f"🚫 [HEIGHT DEBUG] Blocking workbench size recalculation - visible={is_visible}, animating={is_animating}, cooldown={is_cooldown_active}"
            )
            return False

        if is_animating or is_cooldown_active:
            print(
                "🚫 [SYNC DEBUG] Blocking size recalculation during animation/cooldown"
            )
            return False

        return True

    def recalculate_and_apply_size(
        self, is_animating: bool, is_cooldown_active: bool
    ) -> None:
        """Recalculate and apply new size if needed (only when not animating)"""
        if not self.should_recalculate_size(is_animating, is_cooldown_active):
            return

        new_height = self.get_preferred_height()
        current_height = self._graph_editor.height()

        is_visible = (
            hasattr(self._graph_editor, "_state_manager")
            and self._graph_editor.state_manager.is_visible()
        )

        print(
            f"🔍 [HEIGHT DEBUG] Recalculate check: current={current_height}px, new={new_height}px, visible={is_visible}"
        )

        if abs(new_height - current_height) > 5:
            print(
                f"📏 [HEIGHT DEBUG] APPLYING height change: {current_height} -> {new_height} (visible={is_visible})"
            )

            if not is_visible and new_height > 0:
                print(
                    f"🚨 [HEIGHT DEBUG] WARNING: Attempting to set height {new_height}px when graph editor should be collapsed!"
                )
                print(
                    f"🚨 [HEIGHT DEBUG] Call stack trace needed - this should not happen!"
                )
                return

            self._graph_editor.setFixedHeight(new_height)
        else:
            print(
                f"🔍 [HEIGHT DEBUG] Skipping height change: difference {abs(new_height - current_height)}px too small"
            )

    def get_workbench_dimensions(self) -> tuple[int, int]:
        """Get current workbench dimensions"""
        return self._workbench_width, self._workbench_height
