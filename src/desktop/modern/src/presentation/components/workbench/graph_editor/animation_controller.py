from typing import Optional, TYPE_CHECKING
from PyQt6.QtCore import QObject, QPropertyAnimation, QEasingCurve, pyqtSignal, QTimer
import logging

from .animation.animation_size_calculator import AnimationSizeCalculator
from .animation.animation_state_manager import AnimationStateManager
from .animation.animation_synchronizer import AnimationSynchronizer

if TYPE_CHECKING:
    from .graph_editor import GraphEditor

# Set up animation logger
animation_logger = logging.getLogger("tka.animation")


class GraphEditorAnimationController(QObject):
    """
    Clean, focused animation controller for the graph editor.

    This controller coordinates between specialized animation components:
    - AnimationSizeCalculator: Handles size calculations
    - AnimationStateManager: Manages animation state and race conditions
    - AnimationSynchronizer: Synchronizes toggle tab positioning

    Responsibilities:
    - PyQt6 animation setup and coordination
    - Animation lifecycle management (start/stop/finish)
    - Event emission for animation state changes
    - Integration between animation components
    """

    animation_started = pyqtSignal(bool)
    animation_finished = pyqtSignal(bool)

    def __init__(self, graph_editor: "GraphEditor", parent: Optional[QObject] = None):
        super().__init__(parent)
        self._graph_editor = graph_editor

        # Initialize size calculator, state manager, and synchronizer
        self._size_calculator = AnimationSizeCalculator(graph_editor)
        self._state_manager = AnimationStateManager(graph_editor)
        self._synchronizer = AnimationSynchronizer(graph_editor)

        self._height_animation: Optional[QPropertyAnimation] = None

        self._animation_progress_timer: Optional[QTimer] = None

        self._setup_animations()

    def _setup_animations(self) -> None:
        """Setup smooth sliding animation system"""

        self._height_animation = QPropertyAnimation(
            self._graph_editor, b"maximumHeight"
        )
        self._height_animation.setDuration(400)
        self._height_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._height_animation.finished.connect(self._on_animation_finished)
        self._height_animation.valueChanged.connect(self._on_height_animation_progress)

        self._animation_progress_timer = QTimer()
        self._animation_progress_timer.timeout.connect(self._track_animation_progress)
        self._animation_progress_timer.setInterval(50)

    def _on_height_animation_progress(self, value):
        """Track height animation progress"""
        if self._state_manager.is_actively_animating():
            start_height = self._height_animation.startValue()
            end_height = self._height_animation.endValue()
            if start_height is not None and end_height is not None:
                progress = (
                    (value - start_height) / (end_height - start_height)
                    if end_height != start_height
                    else 1.0
                )
                animation_logger.debug(
                    "Animation progress: %d%% (height=%d)", int(progress * 100), value
                )

    def _track_animation_progress(self):
        """Track overall animation progress"""
        if not self._state_manager.is_actively_animating():
            return

        graph_height = self._graph_editor.height()
        toggle_tab = getattr(self._graph_editor, "_toggle_tab", None)

        if toggle_tab:
            start_height = self._height_animation.startValue()
            end_height = self._height_animation.endValue()
            if start_height is not None and end_height is not None:
                progress = (
                    (graph_height - start_height) / (end_height - start_height)
                    if end_height != start_height
                    else 1.0
                )
                progress = max(0.0, min(1.0, progress))

    def update_workbench_size(self, width: int, height: int) -> None:
        """Update workbench size reference for height calculations"""
        self._size_calculator.update_workbench_size(width, height)

        # Check if we should recalculate size after workbench change
        if self._size_calculator.should_recalculate_size(
            self._state_manager.is_actively_animating(),
            self._state_manager.is_in_cooldown(),
        ):
            animation_logger.debug("Workbench size change triggering recalculation")
            self._size_calculator.recalculate_and_apply_size(
                self._state_manager.is_actively_animating(),
                self._state_manager.is_in_cooldown(),
            )

    def get_preferred_height(self) -> int:
        """Calculate preferred height based on workbench dimensions"""
        return self._size_calculator.get_preferred_height()

    def is_animating(self) -> bool:
        """Check if animation is currently in progress or in cooldown period"""
        return self._state_manager.is_animating()

    def validate_state_synchronization(self) -> bool:
        """
        Validate that internal visibility state matches visual state.
        Returns True if synchronized, False if desynchronized.
        Automatically corrects desynchronization when found.
        """
        return self._state_manager.validate_state_synchronization()

    def slide_up(self) -> bool:
        """
        Slide the graph editor up from bottom (show) with consistent height.

        Returns:
            bool: True if animation started, False if already visible or animating
        """

        # Use state manager to check if animation can start and set state
        if not self._state_manager.start_show_animation():
            return False

        self._graph_editor.show()

        preferred_height = self.get_preferred_height()
        self._graph_editor.setFixedHeight(preferred_height)

        self._animation_target_height = self._graph_editor.height()
        animation_logger.debug(
            "Animation target height: %dpx (preferred: %dpx)",
            self._animation_target_height,
            preferred_height,
        )

        self._graph_editor.setMaximumHeight(self._animation_target_height)
        self._graph_editor.setMinimumHeight(0)

        self._height_animation.setStartValue(0)
        self._height_animation.setEndValue(self._animation_target_height)

        animation_logger.debug(
            "Starting slide_up animation: 0 → %d", self._animation_target_height
        )

        self._synchronizer.enable_real_time_sync()

        self._animation_progress_timer.start()

        self._synchronizer.start_synchronized_animations(
            self._height_animation, is_showing=True
        )

        self.animation_started.emit(True)

        return True

    def slide_down(self) -> bool:
        """
        Slide the graph editor down to bottom (hide).

        Returns:
            bool: True if animation started, False if already hidden or animating
        """

        # Use state manager to check if animation can start and set state
        if not self._state_manager.start_hide_animation():
            return False

        current_height = self._graph_editor.height()

        self._graph_editor.setMaximumHeight(16777215)
        self._graph_editor.setMinimumHeight(0)

        self._height_animation.setStartValue(current_height)
        self._height_animation.setEndValue(0)

        animation_logger.debug("Starting slide_down animation: %d → 0", current_height)

        self._synchronizer.enable_real_time_sync()

        self._animation_progress_timer.start()

        self._synchronizer.start_synchronized_animations(
            self._height_animation, is_showing=False
        )

        self.animation_started.emit(False)

        return True

    def _on_animation_finished(self) -> None:
        """Handle animation completion using stored target height"""
        # Determine intended visibility based on target height
        intended_visibility = (
            self._animation_target_height is not None
            and self._animation_target_height > 0
        )

        # Delegate to state manager for proper state handling
        self._state_manager.animation_finished(intended_visibility)

        self._unlock_graph_editor_height_after_animation()

        if self._animation_progress_timer:
            self._animation_progress_timer.stop()

        animation_type = "slide_up" if intended_visibility else "slide_down"
        animation_logger.debug("Animation completed: %s", animation_type)

        self.animation_finished.emit(intended_visibility)

    def _detect_layout_interference(self):
        """Detect if external layout updates are interfering with animations"""
        if not self._state_manager.is_actively_animating():
            return

        current_height = self._graph_editor.height()
        expected_height = (
            self._height_animation.currentValue() if self._height_animation else None
        )

        if expected_height is not None:
            height_discrepancy = abs(current_height - expected_height)
            if height_discrepancy > 5:
                animation_logger.warning(
                    "Layout interference detected: expected_h=%d, actual_h=%d, discrepancy=%dpx",
                    expected_height,
                    current_height,
                    height_discrepancy,
                )

    def _recalculate_size_if_needed(self) -> None:
        """Recalculate and apply new size if needed (only when not animating)"""
        self._size_calculator.recalculate_and_apply_size(
            self._state_manager.is_actively_animating(),
            self._state_manager.is_in_cooldown(),
        )

    def _lock_graph_editor_height_during_animation(self):
        """Lock graph editor height to prevent external layout interference during animation"""

        self._original_size_policy = self._graph_editor.sizePolicy()
        self._original_min_height = self._graph_editor.minimumHeight()
        self._original_max_height = self._graph_editor.maximumHeight()

        from PyQt6.QtWidgets import QSizePolicy

        fixed_policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._graph_editor.setSizePolicy(fixed_policy)

        self._original_resize_event = self._graph_editor.resizeEvent
        self._original_set_fixed_height = self._graph_editor.setFixedHeight

        def locked_resize_event(event):
            animation_logger.debug(
                "Blocked resize event during animation: %dpx", event.size().height()
            )

        def locked_set_fixed_height(height):
            animation_logger.debug(
                "Blocked setFixedHeight during animation: %dpx", height
            )

        self._graph_editor.resizeEvent = locked_resize_event
        self._graph_editor.setFixedHeight = locked_set_fixed_height

        animation_logger.debug("Graph editor height LOCKED during animation")

    def _unlock_graph_editor_height_after_animation(self):
        """Unlock graph editor height to allow normal layout updates after animation"""

        if hasattr(self, "_original_size_policy"):
            self._graph_editor.setSizePolicy(self._original_size_policy)
        if hasattr(self, "_original_min_height"):
            self._graph_editor.setMinimumHeight(self._original_min_height)
        if hasattr(self, "_original_max_height"):
            self._graph_editor.setMaximumHeight(self._original_max_height)

        if hasattr(self, "_original_resize_event"):
            self._graph_editor.resizeEvent = self._original_resize_event
        if hasattr(self, "_original_set_fixed_height"):
            self._graph_editor.setFixedHeight = self._original_set_fixed_height

        animation_logger.debug("Graph editor height UNLOCKED after animation")
