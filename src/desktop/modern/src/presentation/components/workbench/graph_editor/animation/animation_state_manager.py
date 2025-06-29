"""
Animation State Manager
======================

Manages animation state without race conditions. Extracted from the original animation
controller to provide focused, single-responsibility state management.

This class fixes the critical race condition where visibility state was updated before
animation actually started, leading to inconsistent state during animation failures.

Key improvements:
- State is only updated when animation actually starts/completes
- Proper cooldown period management
- Race-condition-free state transitions
- Clear separation between animation state and visibility state
"""

from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import QTimer
import logging

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor

animation_logger = logging.getLogger(__name__)


class AnimationStateManager:
    """Manages animation state without race conditions"""

    def __init__(self, graph_editor: "GraphEditor"):
        self._graph_editor = graph_editor
        self._animating = False
        self._animation_cooldown_active = False
        self._animation_target_height: Optional[int] = None
        self._intended_visibility: Optional[bool] = None
        self._current_visibility: Optional[bool] = (
            None  # Single source of truth during animations
        )

    def is_animating(self) -> bool:
        """Check if animation is currently in progress or in cooldown period"""
        return self._animating or self._animation_cooldown_active

    def can_start_show_animation(self) -> bool:
        """Check if show animation can be started"""
        is_visible = self._get_visibility_state()
        if is_visible or self.is_animating():
            return False
        return True

    def can_start_hide_animation(self) -> bool:
        """Check if hide animation can be started"""
        is_visible = self._get_visibility_state()
        is_animating = self.is_animating()
        if not is_visible or is_animating:
            return False
        return True

    def start_show_animation(self) -> bool:
        """Start show animation - only sets state when animation actually begins"""
        if not self.can_start_show_animation():
            return False

        animation_logger.debug("Starting slide up animation")
        self._animating = True
        self._current_visibility = (
            True  # Set our visibility state as single source of truth
        )

        # Sync with main state manager
        if hasattr(self._graph_editor, "_state_manager"):
            self._graph_editor.state_manager.set_visibility(True, emit_signal=False)

        return True

    def start_hide_animation(self) -> bool:
        """Start hide animation - only sets state when animation actually begins"""
        if not self.can_start_hide_animation():
            return False

        animation_logger.debug("Starting slide down animation")
        self._animating = True
        self._current_visibility = (
            False  # Set our visibility state as single source of truth
        )

        # Sync with main state manager
        if hasattr(self._graph_editor, "_state_manager"):
            self._graph_editor.state_manager.set_visibility(False, emit_signal=False)

        self._animation_target_height = None
        return True

    def animation_finished(self, intended_visibility: bool) -> None:
        """Handle animation completion - starts cooldown period"""
        self._intended_visibility = intended_visibility
        animation_logger.debug(
            "Animation finished. Intended visibility: %s", intended_visibility
        )

        # Start cooldown period to prevent immediate state changes
        self._animation_cooldown_active = True
        QTimer.singleShot(100, self._complete_animation_cleanup)

    def _complete_animation_cleanup(self) -> None:
        """Complete animation cleanup after cooldown period with visual state validation"""
        current_height = self._graph_editor.height()
        intended_visibility = self._intended_visibility

        # Determine actual visual state based on geometry
        visual_state_visible = current_height > 0

        animation_logger.debug(
            "Animation cooldown completed - layout recalculations enabled"
        )
        animation_logger.debug(
            "Post-cooldown state: height=%spx, intended_visible=%s, visual_visible=%s",
            current_height,
            intended_visibility,
            visual_state_visible,
        )

        # Validate intended state against visual reality
        if intended_visibility is not None:
            if intended_visibility != visual_state_visible:
                animation_logger.warning(
                    "State desynchronization detected! Intended: %s, Visual: %s (height=%spx). Correcting to match visual state.",
                    intended_visibility,
                    visual_state_visible,
                    current_height,
                )
                # Correct the state to match visual reality
                corrected_visibility = visual_state_visible
            else:
                corrected_visibility = intended_visibility
        else:
            # No intended state, use visual state
            corrected_visibility = visual_state_visible

        # Apply the corrected visibility state to the graph editor's state manager
        if hasattr(self._graph_editor, "state_manager"):
            self._graph_editor.state_manager.set_visibility(
                corrected_visibility, emit_signal=False
            )
            animation_logger.debug(
                "Applied corrected visibility: %s (intended=%s, visual=%s)",
                corrected_visibility,
                intended_visibility,
                visual_state_visible,
            )

        # Clear all animation state
        self._animating = False
        self._animation_cooldown_active = False
        self._intended_visibility = None
        # Keep _current_visibility until next animation starts - it's our single source of truth

    def get_animation_target_height(self) -> Optional[int]:
        """Get the target height for current animation"""
        return self._animation_target_height

    def set_animation_target_height(self, height: Optional[int]) -> None:
        """Set the target height for current animation"""
        self._animation_target_height = height

    def _get_visibility_state(self) -> bool:
        """Get current visibility state - use our state during animations, fallback to main state manager"""
        # During animations, we are the single source of truth
        if self._current_visibility is not None:
            return self._current_visibility

        # When not animating, check the main state manager
        return (
            hasattr(self._graph_editor, "_state_manager")
            and self._graph_editor.state_manager.is_visible()
        )

    def is_in_cooldown(self) -> bool:
        """Check if animation is in cooldown period"""
        return self._animation_cooldown_active

    def is_actively_animating(self) -> bool:
        """Check if animation is actively running (not in cooldown)"""
        return self._animating and not self._animation_cooldown_active

    def validate_state_synchronization(self) -> bool:
        """
        Validate that internal visibility state matches visual state.
        Returns True if synchronized, False if desynchronized.
        Automatically corrects desynchronization when found.
        """
        animation_logger.debug("validate_state_synchronization() called")

        if self.is_animating():
            # Don't validate during animations
            animation_logger.debug("Skipping validation - animation in progress")
            return True

        animation_logger.debug("Proceeding with validation - no animation in progress")

        current_height = self._graph_editor.height()

        # Always determine visual state based on actual height
        # If height is 0, the graph editor is visually collapsed regardless of constraints
        visual_state_visible = current_height > 0

        internal_state_visible = self._get_visibility_state()

        animation_logger.debug(
            "Validation check: height=%spx, visual=%s, internal=%s",
            current_height,
            visual_state_visible,
            internal_state_visible,
        )

        if visual_state_visible != internal_state_visible:
            animation_logger.warning(
                "State desynchronization detected during validation! Internal: %s, Visual: %s (height=%spx). Auto-correcting.",
                internal_state_visible,
                visual_state_visible,
                current_height,
            )

            # Correct the internal state to match visual reality
            if hasattr(self._graph_editor, "state_manager"):
                self._graph_editor.state_manager.set_visibility(
                    visual_state_visible, emit_signal=False
                )

            # Update our current visibility if we're managing it
            self._current_visibility = visual_state_visible

            animation_logger.debug(
                "State corrected: internal state now matches visual state (%s)",
                visual_state_visible,
            )
            return False  # Was desynchronized

        return True  # Is synchronized
