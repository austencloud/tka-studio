"""
Window Resize Coordinator Service

Coordinates pictograph re-scaling when the main window is resized.
Ensures all pictograph components use the correct main window width for scaling calculations.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from PyQt6.QtCore import QObject, pyqtSignal


@runtime_checkable
class IPictographRescalable(Protocol):
    """Protocol for components that can be re-scaled when window size changes."""

    def rescale_for_window_size(self, main_window_width: int) -> None:
        """Re-scale the pictograph component for the given main window width."""
        ...


class WindowResizeCoordinator(QObject):
    """
    Coordinates pictograph re-scaling when the main window is resized.

    This service maintains a registry of pictograph components that need to be
    re-scaled when the window size changes, ensuring consistent scaling across
    the application.
    """

    # Signal emitted when window is resized with new width
    window_resized = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._registered_components: list[IPictographRescalable] = []
        self._current_window_width: int | None = None
        self._resize_threshold = 50  # Minimum change to trigger re-scaling

        # Connect to our own signal to handle re-scaling
        self.window_resized.connect(self._handle_window_resize)

    def register_component(self, component: IPictographRescalable) -> None:
        """
        Register a pictograph component for automatic re-scaling.

        Args:
            component: Component that implements IPictographRescalable
        """
        if component not in self._registered_components:
            self._registered_components.append(component)

            # If we already have a window width, scale the component immediately
            if self._current_window_width:
                try:
                    component.rescale_for_window_size(self._current_window_width)
                except Exception as e:
                    print(
                        f"⚠️ [RESIZE_COORDINATOR] Error scaling component on registration: {e}"
                    )

    def unregister_component(self, component: IPictographRescalable) -> None:
        """
        Unregister a pictograph component from automatic re-scaling.

        Args:
            component: Component to unregister
        """
        if component in self._registered_components:
            self._registered_components.remove(component)

    def notify_window_resize(self, new_width: int) -> None:
        """
        Notify the coordinator that the window has been resized.

        Args:
            new_width: New main window width in pixels
        """
        # Only trigger re-scaling if the change is significant
        if (
            self._current_window_width is None
            or abs(new_width - self._current_window_width) >= self._resize_threshold
        ):
            self._current_window_width = new_width

            # Emit signal to trigger re-scaling
            self.window_resized.emit(new_width)

    def _handle_window_resize(self, new_width: int) -> None:
        """
        Handle window resize by re-scaling all registered components.

        Args:
            new_width: New main window width in pixels
        """
        if not self._registered_components:
            return

        successful_rescales = 0
        failed_rescales = 0

        for component in self._registered_components[
            :
        ]:  # Copy list to avoid modification during iteration
            try:
                component.rescale_for_window_size(new_width)
                successful_rescales += 1
            except Exception as e:
                print(
                    f"⚠️ [RESIZE_COORDINATOR] Error re-scaling component {type(component).__name__}: {e}"
                )
                failed_rescales += 1

                # Remove components that consistently fail
                if hasattr(component, "_rescale_failures"):
                    component._rescale_failures += 1
                    if component._rescale_failures >= 3:
                        self.unregister_component(component)
                        print(
                            f"⚠️ [RESIZE_COORDINATOR] Removed failing component: {type(component).__name__}"
                        )
                else:
                    component._rescale_failures = 1

    def get_current_window_width(self) -> int | None:
        """
        Get the current main window width.

        Returns:
            Current window width in pixels, or None if not set
        """
        return self._current_window_width

    def force_rescale_all(self) -> None:
        """Force re-scaling of all registered components with current window width."""
        if self._current_window_width:
            self._handle_window_resize(self._current_window_width)

    def clear_all_components(self) -> None:
        """Clear all registered components (useful for cleanup)."""
        self._registered_components.clear()

    def get_component_count(self) -> int:
        """Get the number of registered components."""
        return len(self._registered_components)
